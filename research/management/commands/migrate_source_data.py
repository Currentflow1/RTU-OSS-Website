from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import connections, transaction
from django.db.models import Max

from org.models import Announcement
from research.models import ResearchField, ResearchPaper, ResearchTitle


class Command(BaseCommand):
    help = (
        "Safely migrate application data from the SQLite 'source' database "
        "to PostgreSQL 'default' and upload research PDFs to Supabase Storage."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-files",
            action="store_true",
            help="Migrate database records but do not upload PDFs.",
        )

    def handle(self, *args, **options):
        skip_files = options["skip_files"]

        self.stdout.write(self.style.WARNING(
            "Starting source-data migration..."
        ))

        self.verify_connections()

        source_counts = self.get_source_counts()

        self.stdout.write("")
        self.stdout.write("SOURCE DATABASE")
        self.stdout.write(
            f"Users:             {source_counts['users']}"
        )
        self.stdout.write(
            f"Research fields:   {source_counts['fields']}"
        )
        self.stdout.write(
            f"Research titles:   {source_counts['titles']}"
        )
        self.stdout.write(
            f"Research papers:   {source_counts['papers']}"
        )
        self.stdout.write(
            f"Announcements:     {source_counts['announcements']}"
        )
        self.stdout.write(
            f"Titles with user:  {source_counts['submitted_titles']}"
        )

        self.stdout.write("")

        if not all(source_counts.values()):
            raise CommandError(
                "One or more source counts are zero. "
                "Refusing to continue automatically."
            )

        with transaction.atomic(using="default"):
            self.migrate_users()
            self.migrate_research_fields()
            self.migrate_research_titles()
            self.migrate_research_papers()
            self.migrate_announcements()

        self.reset_sequences()

        if skip_files:
            self.stdout.write("")
            self.stdout.write(
                self.style.WARNING(
                    "PDF upload skipped because --skip-files was supplied."
                )
            )
        else:
            self.upload_pdfs()

        self.print_target_counts()

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "Source-data migration completed."
            )
        )

    def verify_connections(self):
        source = connections["source"]
        default = connections["default"]

        source.ensure_connection()
        default.ensure_connection()

        if source.vendor != "sqlite":
            raise CommandError(
                f"Expected source database to be SQLite, got {source.vendor}."
            )

        if default.vendor != "postgresql":
            raise CommandError(
                f"Expected default database to be PostgreSQL, got {default.vendor}."
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Database connections verified: SQLite -> PostgreSQL"
            )
        )

    def get_source_counts(self):
        User = get_user_model()

        return {
            "users": User.objects.using("source").count(),
            "fields": ResearchField.objects.using("source").count(),
            "titles": ResearchTitle.objects.using("source").count(),
            "papers": ResearchPaper.objects.using("source").count(),
            "announcements": Announcement.objects.using("source").count(),
            "submitted_titles": ResearchTitle.objects.using("source")
            .filter(submitted_by__isnull=False)
            .count(),
        }

    def migrate_users(self):
        User = get_user_model()

        source_users = User.objects.using("source").all().order_by("pk")

        self.stdout.write("Migrating users...")

        for source_user in source_users:
            target_user, created = User.objects.using("default").get_or_create(
                pk=source_user.pk,
                defaults={
                    field.name: getattr(source_user, field.name)
                    for field in User._meta.concrete_fields
                    if field.name != "id"
                },
            )

            if not created:
                update_fields = []

                for field in User._meta.concrete_fields:
                    if field.name == "id":
                        continue

                    value = getattr(source_user, field.name)

                    if getattr(target_user, field.name) != value:
                        setattr(target_user, field.name, value)
                        update_fields.append(field.name)

                if update_fields:
                    target_user.save(
                        using="default",
                        update_fields=update_fields,
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"  Users migrated: {source_users.count()}"
            )
        )

    def migrate_research_fields(self):
        source_fields = (
            ResearchField.objects
            .using("source")
            .all()
            .order_by("pk")
        )

        self.stdout.write("Migrating research fields...")

        for source_field in source_fields:
            ResearchField.objects.using("default").update_or_create(
                pk=source_field.pk,
                defaults={
                    "name": source_field.name,
                    "slug": source_field.slug,
                    "description": source_field.description,
                    "created_at": source_field.created_at,
                    "updated_at": source_field.updated_at,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"  Research fields migrated: {source_fields.count()}"
            )
        )

    def migrate_research_titles(self):
        source_titles = (
            ResearchTitle.objects
            .using("source")
            .all()
            .order_by("pk")
        )

        self.stdout.write("Migrating research titles...")

        for source_title in source_titles:
            ResearchTitle.objects.using("default").update_or_create(
                pk=source_title.pk,
                defaults={
                    "research_field_id": source_title.research_field_id,
                    "title": source_title.title,
                    "slug": source_title.slug,
                    "description": source_title.description,
                    "authors": source_title.authors,
                    "keywords": source_title.keywords,
                    "department": source_title.department,
                    "program": source_title.program,
                    "adviser": source_title.adviser,
                    "school_year": source_title.school_year,
                    "publication_date": source_title.publication_date,
                    "created_at": source_title.created_at,
                    "updated_at": source_title.updated_at,
                    "submitted_by_id": source_title.submitted_by_id,
                    "submitter_email": source_title.submitter_email,
                    "publication_status": source_title.publication_status,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"  Research titles migrated: {source_titles.count()}"
            )
        )

    def migrate_research_papers(self):
        source_papers = (
            ResearchPaper.objects
            .using("source")
            .all()
            .order_by("pk")
        )

        self.stdout.write("Migrating research paper records...")

        for source_paper in source_papers:
            ResearchPaper.objects.using("default").update_or_create(
                pk=source_paper.pk,
                defaults={
                    "research_title_id": source_paper.research_title_id,
                    "abstract": source_paper.abstract,
                    "document": source_paper.document.name,
                    "created_at": source_paper.created_at,
                    "updated_at": source_paper.updated_at,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"  Research paper records migrated: {source_papers.count()}"
            )
        )

    def migrate_announcements(self):
        source_announcements = (
            Announcement.objects
            .using("source")
            .all()
            .order_by("pk")
        )

        self.stdout.write("Migrating announcements...")

        for source_announcement in source_announcements:
            Announcement.objects.using("default").update_or_create(
                pk=source_announcement.pk,
                defaults={
                    "title": source_announcement.title,
                    "slug": source_announcement.slug,
                    "summary": source_announcement.summary,
                    "content": source_announcement.content,
                    "published_at": source_announcement.published_at,
                    "created_at": source_announcement.created_at,
                    "updated_at": source_announcement.updated_at,
                    "is_published": source_announcement.is_published,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"  Announcements migrated: {source_announcements.count()}"
            )
        )

    def upload_pdfs(self):
        source_papers = (
            ResearchPaper.objects
            .using("source")
            .select_related("research_title")
            .all()
            .order_by("pk")
        )

        source_db_path = Path(
            connections["source"].settings_dict["NAME"]
        )

        project_root = source_db_path.parent
        media_root = project_root / "media"

        if not media_root.exists():
            raise CommandError(
                f"Media directory does not exist: {media_root}"
            )

        from django.core.files.storage import default_storage

        self.stdout.write("")
        self.stdout.write("Uploading PDFs to Supabase Storage...")

        uploaded = 0
        skipped = 0
        missing = 0

        for index, source_paper in enumerate(source_papers, start=1):
            document_name = source_paper.document.name

            if not document_name:
                missing += 1
                continue

            local_path = media_root / document_name

            if not local_path.exists():
                self.stdout.write(
                    self.style.ERROR(
                        f"  Missing local PDF: {local_path}"
                    )
                )
                missing += 1
                continue

            if default_storage.exists(document_name):
                skipped += 1
            else:
                with local_path.open("rb") as pdf_file:
                    default_storage.save(
                        document_name,
                        File(pdf_file),
                    )

                uploaded += 1

            if index % 100 == 0:
                self.stdout.write(
                    f"  Processed PDFs: {index}/{source_papers.count()}"
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"  PDFs uploaded: {uploaded}"
            )
        )
        self.stdout.write(
            f"  PDFs already present: {skipped}"
        )

        if missing:
            self.stdout.write(
                self.style.ERROR(
                    f"  PDFs missing locally: {missing}"
                )
            )

            raise CommandError(
                "One or more PDFs could not be found. "
                "Database records were migrated, but PDF migration "
                "did not complete."
            )

    def reset_sequences(self):
        models = [
            get_user_model(),
            ResearchField,
            ResearchTitle,
            ResearchPaper,
            Announcement,
        ]

        connection = connections["default"]

        statements = connection.ops.sequence_reset_sql(
            no_style(),
            models,
        )

        if not statements:
            return

        self.stdout.write("Resetting PostgreSQL sequences...")

        with connection.cursor() as cursor:
            for statement in statements:
                cursor.execute(statement)

        self.stdout.write(
            self.style.SUCCESS(
                "  PostgreSQL sequences reset."
            )
        )
        
    def print_target_counts(self):
        User = get_user_model()

        target_titles_with_user = (
            ResearchTitle.objects
            .using("default")
            .filter(submitted_by__isnull=False)
            .count()
        )

        self.stdout.write("")
        self.stdout.write("TARGET DATABASE")

        self.stdout.write(
            f"Users:             {User.objects.using('default').count()}"
        )
        self.stdout.write(
            f"Research fields:   "
            f"{ResearchField.objects.using('default').count()}"
        )
        self.stdout.write(
            f"Research titles:   "
            f"{ResearchTitle.objects.using('default').count()}"
        )
        self.stdout.write(
            f"Research papers:   "
            f"{ResearchPaper.objects.using('default').count()}"
        )
        self.stdout.write(
            f"Announcements:     "
            f"{Announcement.objects.using('default').count()}"
        )
        self.stdout.write(
            f"Titles with user:  {target_titles_with_user}"
        )


def no_style():
    from django.core.management.color import no_style as django_no_style

    return django_no_style()