import random
from django.core.management.base import BaseCommand
from twitter.models import User, Post, Follow
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with fake users, posts, and follows"

    def handle(self, *args, **kwargs):
        self.stdout.write("🧹 Limpando dados antigos...")
        Follow.objects.all().delete()
        Post.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write("👥 Criando usuários...")
        users = []
        for _ in range(10):
            user = User.objects.create_user(
                email=fake.unique.email(),
                username=fake.unique.user_name(),
                password='password123'
            )
            users.append(user)

        self.stdout.write("✍️ Criando posts...")
        for user in users:
            for _ in range(random.randint(1, 5)):
                Post.objects.create(
                    author=user,
                    content=fake.paragraph(nb_sentences=3)
                )

        self.stdout.write("🔗 Criando follows...")
        for user in users:
            others = [u for u in users if u != user]
            followed = random.sample(others, k=random.randint(1, len(others) // 2))
            for f in followed:
                Follow.objects.get_or_create(follower=user, following=f)

        self.stdout.write(self.style.SUCCESS("✅ Dados de teste criados com sucesso!"))
