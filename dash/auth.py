from django.contrib.auth.backends import ModelBackend
from .utils import *
from .models import SkyUser
from .auth_utils.permissions import update_user_perms
from .auth_utils.utils import getUserDetails
import pandas as pd

class SkyAuthentication(ModelBackend):
    def authenticate(self, request, token=None):
        user = getUserDetails(token)

        # Calling the sky api
        user = sky.get(f"users/extended/{user['user_id']}", raw_data=True)

        if user.get('errors'):
            return None

        # User's biographical data, in dictionary
        user_bio = pd.json_normalize(user)[['id', 'email', 'first_name', 'last_name', 'preferred_name', 'student_id']].to_dict(orient='records')[0]

        # User's Blackbaud roles, in list
        roles = pd.json_normalize(user, 'roles').name.tolist()  
        user_bio['roles'] = roles
        
        # User's children, in list
        relationships = pd.json_normalize(user, 'relationships')    
        if not relationships.empty:
            # Continuing if the user has relationships
            relationships = relationships[relationships.user_one_role.isin(['Parent'])]
            if not relationships.empty:
                # Continuting if the user has children
                relationships['full_name'] = relationships.last_name.map(str) + " " + relationships.first_name
                # Cleaning the kid data
                kids = relationships[['full_name', 'user_two_id']].rename(columns={'user_two_id':'id'}).reset_index()
                # Creating unique ids for tags 
                kids['index'] = kids['index'].apply(lambda x: 'child' + str(x))
                # Saving as nested dict
                kids = kids.to_dict(orient='records')
            else:
                kids = None
        else:
            kids = None
        # Storing the users data in a session
        request.session['kids'] = kids

        # Cleaning student id 
        if str(user_bio['student_id']) == '':
            user_bio.pop('student_id')

        print('About to search for user')
        print(user_bio)
        try:
            # Updating the User data
            SkyUser.objects.filter(pk=user_bio['id']).update(**user_bio)

            # Updating the user's perms
            update_user_perms(user_bio['id'], roles)

            # Getting the user
            user = SkyUser.objects.get(pk=user_bio['id'])
        # except SkyUser.DoesNotExist:
        except Exception as e:
            print(e)
            user = SkyUser.objects.create_user(user_bio)
        return user

    def get_user(self, user_id):
        try:
            return SkyUser.objects.get(pk=user_id)
        except SkyUser.DoesNotExist:
            return None