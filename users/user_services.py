from .models import User, CustomUser, UserSubscribers, UserSubscriptions


def select_current_user_and_user_info(username):
    """Get user and user_info form user with current username"""
    user = User.objects.get(username=username)
    user_info = CustomUser.objects.get(user=user.id)

    return user, user_info


def create_new_user_and_custom_user(username, password):
    """Create user and user detail objects"""
    user = User.objects.create_user(
        username=username,
        password=password
    )
    CustomUser.objects.create(user=user)

    return user


def edit_current_user_personal_data(request, username):
    """Get current user by username and change his data gotten from the form"""
    user, user_info = select_current_user_and_user_info(username)

    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.username = request.POST['username']
    user.email = request.POST['email']
    if request.POST['profile_photo'] != '':
        user_info.profile_photo = request.POST['profile_photo']
    user_info.description = request.POST['description']
    user.save()
    user_info.save()


def add_subscriber_and_subscription_to_user(request, username):
    """Add user subscriptions and subscriber fot subscribed user"""
    user_who_subscribe = CustomUser.objects.get(user=request.user.id)

    user_subscribe_to = User.objects.get(username=username)
    user_for_subscribe_info = CustomUser.objects.get(user=user_subscribe_to.id)

    subscription = UserSubscriptions.objects.get_or_create(user=user_for_subscribe_info.user)
    subscriber = UserSubscribers.objects.get_or_create(user=User.objects.get(id=request.user.id))

    user_who_subscribe.subscriptions.add(subscription[0])
    user_for_subscribe_info.subscribers.add(subscriber[0])

    user_who_subscribe.save()
    user_for_subscribe_info.save()


def get_all_users():
    return User.objects.all()
