from bot import InstagramBot
from Config import Software

if __name__ == '__main__':

    Software.instagram_app_header()
    instagram = InstagramBot('username', 'password')
