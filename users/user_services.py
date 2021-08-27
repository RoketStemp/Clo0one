from .models import User, CustomUser, UserSubscribers, UserSubscriptions


def select_current_user_and_user_info_by_username_or_user_id(username=None, user_id=None):
    """Get user and user_info form user with current username"""
    if username:
        user = User.objects.get(username=username)
        user_info = CustomUser.objects.get(user=user.id)
    else:
        user = User.objects.get(id=user_id)
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


def edit_current_user_personal_data(
        new_first_name, new_last_name, new_username, new_email,
        new_profile_photo, new_description, username
):
    """Get current user by username and change his data gotten from the form"""
    user, user_info = select_current_user_and_user_info(username)

    user.first_name = new_first_name
    user.last_name = new_last_name
    user.username = new_username
    user.email = new_email
    if new_profile_photo != '':
        user_info.profile_photo = new_profile_photo
    user_info.description = new_description
    user.save()
    user_info.save()

    return user.username


def add_or_remove_subscriber_and_subscription_to_user(current_user_id, username, action):
    """Add or remove user subscriptions and subscriber for subscribed user, which depends on action argument"""
    user_who_subscribe = CustomUser.objects.get(user=current_user_id)

    user_subscribe_to = User.objects.get(username=username)
    user_for_subscribe_info = CustomUser.objects.get(user=user_subscribe_to.id)

    subscription = UserSubscriptions.objects.get_or_create(user=user_for_subscribe_info.user)
    subscriber = UserSubscribers.objects.get_or_create(user=User.objects.get(id=current_user_id))

    if action == 'add':
        user_who_subscribe.subscriptions.add(subscription[0])
        user_for_subscribe_info.subscribers.add(subscriber[0])
    elif action == 'remove':
        user_who_subscribe.subscriptions.remove(subscription[0])
        user_for_subscribe_info.subscribers.remove(subscriber[0])

    user_who_subscribe.save()
    user_for_subscribe_info.save()


def get_all_users():
    return User.objects.all()


def get_current_user_subscriptions(subscriptions):
    user_subscriptions = []
    for subscription in subscriptions:
        user_subscriptions.append(subscription.user.id)
    return user_subscriptions
