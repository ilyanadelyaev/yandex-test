import django.test

import core.models
import view.views


class DirectionViewTests(django.test.TestCase):
    def test__DetailView_get_context_data(self):
        d = core.models.Direction(name='D')
        v = view.views.DirectionDetailView()
        v.object = d
        t = v.get_context_data()
        self.assertIn('directionstation_list', t)
        self.assertIn('route_list', t)
