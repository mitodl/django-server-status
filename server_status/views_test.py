"""
Tests for the status module.
"""
from __future__ import unicode_literals

from copy import deepcopy
import json
import logging
from freezegun import freeze_time
import mock
from ddt import ddt, data

from django.conf import settings

from django.test import Client
from django.test.utils import override_settings
from django.test.testcases import TestCase
from django.urls import reverse

from server_status import views


log = logging.getLogger(__name__)

HTTP_OK = 200
SERVICE_UNAVAILABLE = 503


@ddt
class TestStatus(TestCase):
    """Test output of status page."""

    def setUp(self):
        """
        Set up client and remember settings for PostgreSQL, Redis,
        and Elasticsearch. Changes made to django.conf.settings during
        tests persist beyond the test scope, so if they are changed
        we need to restore them.
        """

        # Create test client.
        self.client = Client()
        self.url = reverse("status")
        super(TestStatus, self).setUp()

    def get(self, expected_status=HTTP_OK):
        """Get the page."""
        resp = self.client.get(self.url, data={"token": settings.STATUS_TOKEN})
        self.assertEqual(resp.status_code, expected_status,
                         resp.content.decode('utf-8'))
        return json.loads(resp.content.decode('utf-8'))

    def test_view(self):
        """Get normally."""
        with mock.patch(
            'celery.task.control.inspect', autospec=True,
        ) as mocked, mock.patch(
            'celery.Celery', autospec=True
        ):
            mocked.return_value.stats.return_value = {'foo': 'bar'}
            resp = self.get()
        for key in ("postgresql", "redis", "elasticsearch", "celery"):
            self.assertTrue(resp[key]["status"] == views.UP)

        self.assertTrue(resp["status_all"] == views.UP)

    @freeze_time("3000-01-14")
    @override_settings(HEALTH_CHECK=['CERTIFICATE'])
    def test_certificate_status_fail(self):
        """
        test when app certificate is expire.
        datetime.now() == 3000-01-14
        app_cert_expires == 2019-09-18T12:59:16
        """
        resp = self.get(expected_status=SERVICE_UNAVAILABLE)
        assert resp['certificate']["status"] == views.DOWN

    @freeze_time("2018-01-14")
    @override_settings(HEALTH_CHECK=['CERTIFICATE'])
    def test_certificate_status_pass(self):
        """
        test when app certificate is not expire.
        datetime.now() == 2018-01-14
        app_cert_expires == 2019-09-18T12:59:16
        """
        resp = self.get(expected_status=HTTP_OK)
        assert resp['certificate']["status"] == views.UP

    @data(None, "")
    @override_settings(HEALTH_CHECK=['CERTIFICATE'])
    def test_status_invalid_certificate(self, certificate):
        """
        test status when app certificate in not valid.
        """
        with override_settings(MIT_WS_CERTIFICATE=certificate):
            resp = self.get(expected_status=HTTP_OK)
            assert resp['certificate']["status"] == views.NO_CONFIG

    @override_settings(HEALTH_CHECK=['REDIS'])
    def test_redis_with_different_names(self):
        """
        Redis configuration can be called in different names
        """
        # remove the default one that should be in the settings (it should be tested in test_view)
        assert hasattr(settings, 'BROKER_URL')
        assert not hasattr(settings, 'REDIS_URL')
        redis_url = settings.BROKER_URL
        del settings.BROKER_URL
        with override_settings(CELERY_BROKER_URL=redis_url):
            resp = self.get()
            assert resp['redis']["status"] == views.UP
        with override_settings(REDIS_URL=redis_url):
            resp = self.get()
            assert resp['redis']["status"] == views.UP

    @override_settings(USE_CELERY=False)
    def test_no_settings(self):
        """Missing settings."""
        (celery_broker_url, broker_url, databases, elastic_connections) = (
            settings.CELERY_BROKER_URL,
            settings.BROKER_URL,
            settings.DATABASES,
            settings.ELASTICSEARCH_URL
        )
        try:
            del settings.CELERY_BROKER_URL
            del settings.BROKER_URL
            del settings.DATABASES
            del settings.ELASTICSEARCH_URL
            resp = self.get()
            for key in ("postgresql", "redis", "elasticsearch", "celery"):
                self.assertTrue(resp[key]["status"] == views.NO_CONFIG)
        finally:
            (
                settings.CELERY_BROKER_URL,
                settings.BROKER_URL,
                settings.DATABASES,
                settings.ELASTICSEARCH_URL,
            ) = (celery_broker_url, broker_url, databases, elastic_connections)

    def test_broken_settings(self):
        """Settings that couldn't possibly work."""
        junk = " not a chance "
        databases = deepcopy(settings.DATABASES)
        databases['default'] = junk
        with self.settings(
            CELERY_BROKER_URL=junk,
            REDIS_URL='redis://{}'.format(junk),
            DATABASES=databases,
            ELASTICSEARCH_URL=junk,
        ):
            resp = self.get(SERVICE_UNAVAILABLE)
            for key in ("celery", "postgresql", "redis", "elasticsearch"):
                self.assertTrue(resp[key]["status"] == views.DOWN,
                                "%s - %s" % (key, resp[key]))

    def test_invalid_settings(self):
        """
        Settings that look right, but aren't (if service is actually down).
        """
        databases = deepcopy(settings.DATABASES)
        databases["default"]["HOST"] = "monkey"
        with self.settings(
            BROKER_URL="redis://bogus:6379/4",
            DATABASES=databases,
            ELASTICSEARCH_URL="pizza:2300"
        ):
            resp = self.get(SERVICE_UNAVAILABLE)
            for key in ("postgresql", "redis", "elasticsearch"):
                self.assertTrue(resp[key]["status"] == views.DOWN)

    def test_token(self):
        """
        Caller must have correct token, or no dice. Having a good token
        is tested in all the other tests.
        """

        # No token.
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 404, resp.content)

        # Invalid token.
        resp = self.client.get(self.url, {"token": "gibberish"})
        self.assertEqual(resp.status_code, 404, resp.content)

    @override_settings(STATUS_TOKEN="")
    def test_empty_token(self):
        """
        An empty token should not work even if it matches the setting.
        """
        resp = self.client.get(self.url, {"token": ""})
        self.assertEqual(resp.status_code, 404, resp.content)

    def test_celery_errors(self):
        """
        Specific test for celery errors
        """
        # no answer in the stats call
        with mock.patch('celery.task.control.inspect', autospec=True) as mocked:
            mocked.return_value.stats.return_value = {}
            resp = self.get(503)
        self.assertIn("celery", resp)
        self.assertIn("status", resp["celery"])
        self.assertEqual(resp["celery"]["status"], views.DOWN)

        # exception in the stats call
        with mock.patch('celery.task.control.inspect', autospec=True) as mocked:
            mocked.side_effect = IOError()
            resp = self.get(503)
        self.assertIn("celery", resp)
        self.assertIn("status", resp["celery"])
        self.assertEqual(resp["celery"]["status"], views.DOWN)

    def test_status_all(self):
        """
        Test that status_all is DOWN when another service is DOWN
        """
        with mock.patch('celery.task.control.inspect', autospec=True) as mocked:
            mocked.return_value.stats.return_value = {}
            resp = self.get(503)

        self.assertIn("status_all", resp)
        self.assertEqual(resp["status_all"], views.DOWN)
