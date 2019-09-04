import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from dashboard import context_processors
import re
from .models import User, Role, User_role
from .salting_hashing import get_salt, hash_string
from django.contrib import messages


class Users_index(View):
    def get(self, request):
        context = context_processors.base_variables_all(request)
        user_list = User.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(user_list, len(user_list))
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        context["users_data"] = users
        return render(request, 'account/users.html', context)


class Users_delete(View):
    def post(self, request):
        users_id = request.POST["users_id"]
        users_id_list = list(json.loads(users_id))
        if not users_id_list:
            messages.error(request, 'select one of the users')
        elif users_id_list.__contains__(str(request.session['user'])):
            messages.error(request, 'Logged in user cannot be deleted')
        else:
            username_list = []
            for user_id in users_id_list:
                user = User.objects.filter(id=user_id)
                if user:
                    username = user.values_list("username", flat=True)[0]
                    username_list.append(username)
                    user.delete()
                    user_group = User_role.objects.filter(user_id=user_id)
                    if user_group:
                        user_group.delete()

            messages.success(request, '%s successfully deleted' % username_list)
        data = {
            'success': True
        }
        return JsonResponse(data)


class Add_user(View):
    def get(self, request):
        context = context_processors.base_variables_all(request)
        return render(request, 'account/add_user.html', context)

    def post(self, request):
        context = context_processors.base_variables_all(request)

        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if self.username_exists(username):
                if self.username_validate_pattern(username):
                    if self.password_validate_length(password1):
                        if self.password_validate_numeric(password1):
                            if self.confirm_password(password1, password2):
                                salt = get_salt()
                                hashed_password = hash_string(salt, password1)
                                User.objects.create(username=username, salt=salt, hashed_password=hashed_password)
                                user_id = User.objects.get(username=username).id
                                context["success_msg"] = "successfully added user"
                                messages.success(request, '%s successfully added' % username)
                                if "addanother" in request.POST:
                                    return redirect('add_user')
                                elif "continue" in request.POST:
                                    return redirect('change_user', id=user_id)
                            else:
                                context["error_msg"] = "password mismatched"
                        else:
                            context["error_msg"] = "password is all numeric"
                    else:
                        context["error_msg"] = "password length is less than 8"
                else:
                    context["error_msg"] = "username pattern is invalid"
        else:
            context["error_msg"] = "username already exists"

        context["username"] = username
        context["password1"] = password1
        context["password2"] = password2

        return render(request, 'account/add_user.html', context)

    @staticmethod
    def username_exists(username):
        username = User.objects.filter(username=username)
        if username:
            return False
        else:
            return True

    @staticmethod
    def username_validate_length(username):
        if len(username) >= 5:
            return True
        else:
            return False

    @staticmethod
    def username_validate_pattern(username):
        if re.match("^([a-zA-Z0-9]+)[@/./+/-/_ ]*([a-zA-Z0-9]+)$", username):
            return True
        else:
            return False

    @staticmethod
    def password_validate_length(password):
        if len(password) >= 8:
            return True
        else:
            return False

    @staticmethod
    def password_validate_numeric(password):
        if password.isnumeric():
            return False
        else:
            return True

    @staticmethod
    def confirm_password(password1, password2):
        if password1 == password2:
            return True
        else:
            return False


class Change_user(View):
    @staticmethod
    def get(request, id):
        context = context_processors.base_variables_all(request)
        user = User.objects.filter(id=id)
        groups = Role.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(groups, 1)
        try:
            groups = paginator.page(page)
        except PageNotAnInteger:
            groups = paginator.page(1)
        except EmptyPage:
            groups = paginator.page(paginator.num_pages)
        if user:
            context["user_data"] = user.values()[0]
            # context["user_id"] = int(id)
            # print(context["user_data"]["id"], context["user_id"])
            context["groups"] = groups
            user_groups = User_role.objects.filter(user_id=id)
            if user_groups:
                context["user_groups"] = list(user_groups.values_list("role_id", flat=True))
        else:
            messages.error(request, "user doesnot exist")
            return render(request, 'account/users.html', context)

        return render(request, 'account/change_user.html', context)

    @staticmethod
    def post(request, id):

        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        is_active = request.POST["is_active"]
        is_superuser = request.POST["is_superuser"]
        self_user = request.POST["self_user"]
        groups_id = request.POST["groups_id"]
        groups_id_lists = list(json.loads(groups_id))

        if username != '':
            if Add_user().username_validate_pattern(username):
                if Add_user().username_validate_length(username):
                    user = User.objects.filter(id=id)
                    if user:
                        if self_user == "True":
                            print("the user is self")
                            user.update(username=username, email=email, first_name=first_name, last_name=last_name)
                        else:
                            print("the user is not self")
                            user.update(username=username, email=email, first_name=first_name, last_name=last_name,
                                        is_active=is_active, is_superuser=is_superuser)

                            user_groups = User_role.objects.filter(user_id=id)
                            if user_groups:
                                user_groups.delete()

                            if groups_id_lists:
                                for groups_id in groups_id_lists:
                                    User_role.objects.create(user_id=id, role_id=int(groups_id))

                    messages.success(request, '%s successfully changed' % username)
                    success = True
                else:
                    success = False
                    messages.error(request, "%s user name is < 5" % username)
            else:
                success = False
                messages.error(request, "user name is not in given pattern")
        else:
            success = False
            messages.error(request, "user name must not be empty")

        data = {
            'success': success
        }
        return JsonResponse(data)

class Change_password(View):
    def get(self, request, id):
        user_data = User.objects.get(id=id)
        context = context_processors.base_variables_all(request)
        context['user_data'] = user_data
        # print(context['user_data'].username)
        return render(request, 'account/change_password.html', context)


    def post(self, request, id):
        user_data = User.objects.get(id=id)
        old_password = request.POST["old_password"]
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]

        hashed_password = hash_string(user_data.salt, old_password)
        if hashed_password == user_data.hashed_password:
            if Add_user.password_validate_length(new_password):
                if Add_user.password_validate_numeric(new_password):
                    if new_password == confirm_password:
                        salt = get_salt()
                        password = hash_string(salt, new_password)
                        User.objects.filter(id=id).update(salt=salt, hashed_password=password)
                        messages.success(request, 'password for %s successfully changed' % user_data.username)
                        success = True
                    else:
                        success = False
                        messages.error(request, "new password and confirm password did not match")
                else:
                    success = False
                    messages.error(request, "password cannot be all numeric")
            else:
                success = False
                messages.error(request, "length of password must be greater or equal to 8")
        else:
            success = False
            messages.error(request, "old_password incorrect")

        data = {
            'success': success
        }
        return JsonResponse(data)
