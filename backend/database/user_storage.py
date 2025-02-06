from utils.security import password_hash
user_info_dict = {}

def set_user_info(user_info):
    user_info_dict["user_name"] = user_info.user_name
    user_info_dict["email_ID"] = user_info.email_ID
    user_info_dict["password"] = password_hash(user_info.password)
    user_info_dict["signup_time"] = user_info.signup_time
    user_info_dict["time_zone"] = user_info.time_zone
    user_info_dict["privacy_link"] = user_info.privacy_link

def get_user_info():
    return user_info_dict

def database_emails():
    database_user_emails = {"mohitnarayanvashisth2703@gmail.com", "mohitvashisth2703@gmail.com", "3rminds@gmail.com"}  # sample database emails
    return database_user_emails