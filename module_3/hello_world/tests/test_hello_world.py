from freezegun import freeze_time
from datetime import datetime
import datetime
import unittest


from module_3.hello_world.hello_world import app

class TestHelloWorld(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/hello-world/'

    def test_can_get_username(self):
        username = 'username'
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue(username in response_text)

    def test_can_get_right_weekday(self):
        username = 'Хорошей среды'
        days = [datetime.datetime(2024, 4, day) for day in range(1, 8)]
        weekdays_tuple = ('понедельника', 'вторника', 'среды',
                          'четверга', 'пятницы', 'субботы', 'воскресения')
        for day in days:
            with freeze_time(day):
                day = day.weekday()
                date = weekdays_tuple[day]
                response = self.app.get(self.base_url + username)
                response_text = response.data.decode()
                self.assertTrue(((response_text.upper().count(date.upper()) == 1) and (date.upper() not in username.upper()))
                                or response_text.upper().count(date.upper()) == 2)