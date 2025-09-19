# src/automotive_nlp/cli.py
import typer
from sqlalchemy.exc import SQLAlchemyError
from automotive_nlp.db import database, models
from automotive_nlp.db.schemas import FeedbackCreate, FeedbackRead
from automotive_nlp.services.feedback_service import save_feedback
from automotive_nlp.services.analysis_service import analyze_feedback

app = typer.Typer(help="Automotive NLP CLI")

def init_db():
    """Ensure all tables exist."""
    models.Base.metadata.create_all(bind=database.engine)

# ----------------------------
# Add Feedback Command
# ----------------------------
@app.command()
def add_feedback(
    car_make: str = typer.Option(..., prompt=True, help="Manufacturer of the car"),
    car_model: str = typer.Option(..., prompt=True, help="Model of the car"),
    text: str = typer.Option(..., prompt=True, help="Feedback text from customer"),
):
    """Add a feedback item to the database."""
    init_db()
    db = database.SessionLocal()
    try:
        payload = FeedbackCreate(text=text, car_make=car_make, car_model=car_model)
        fb = save_feedback(db, payload)
        db.commit()
        db.refresh(fb)
        typer.secho("✅ Feedback saved", fg=typer.colors.GREEN)
        typer.echo(FeedbackRead.from_orm(fb).model_dump_json(indent=2))
    except (ValueError, SQLAlchemyError) as e:
        db.rollback()
        typer.secho(f"❌ Failed to save feedback: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    finally:
        db.close()

# ----------------------------
# Analyze Feedback Command
# ----------------------------
@app.command()
def analyze(
    n_clusters: int = typer.Argument(
        5,
        help="Number of clusters to form (positional argument, default=5)"
    ),
    cluster_by_make: bool = typer.Option(
        False,
        "--cluster-by-make",
        "-m",
        is_flag=True,
        help="Cluster by car make/model instead of complaint text",
    ),
    alpha: float = typer.Option(
        0.1,
        "--alpha",
        help="Factor for dynamic pricing sensitivity",
    ),
    cap: float = typer.Option(
        0.5,
        "--cap",
        help="Maximum cap on price increase (e.g. 0.5 = +50%)",
    ),
):
    """Run clustering analysis and show suggestions (pricing, sentiment)."""
    init_db()
    db = database.SessionLocal()
    try:
        results = analyze_feedback(
            db,
            cluster_by_make=cluster_by_make,
            n_clusters=n_clusters,
            alpha=alpha,
            cap=cap,
        )
        db.commit()
        if not results:
            typer.secho("⚠️  No feedbacks to analyze.", fg=typer.colors.YELLOW)
            raise typer.Exit(code=0)

        typer.secho("🔍 Analysis results:", fg=typer.colors.CYAN)
        for r in results:
            cap_str = " (capped)" if r.get("capped") else ""
            typer.echo(f"\nCluster: {r['cluster']}  —  count: {r['count']}")
            typer.echo(f"  avg_sentiment: {r['avg_sentiment']:.2f}")
            typer.echo(f"  suggested_cost: ${r['suggested_cost']}{cap_str}")
            typer.echo("  examples:")
            for ex in r["examples"]:
                typer.echo(f"    - {ex}")
    except SQLAlchemyError as e:
        db.rollback()
        typer.secho(f"❌ Analysis failed: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    finally:
        db.close()

# ----------------------------
# CLI Entry
# ----------------------------
if __name__ == "__main__":
    app()
