import factory


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'users.CustomUser'

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.django.Password('pw')
