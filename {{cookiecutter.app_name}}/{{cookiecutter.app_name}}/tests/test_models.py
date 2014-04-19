# -*- coding: utf-8 -*-
import unittest
import datetime as dt
from nose.tools import *  # PEP8 asserts

from {{ cookiecutter.app_name }}.database import db
from {{ cookiecutter.app_name }}.user.models import User, Role
from .base import DbTestCase
from .factories import UserFactory


class TestUser(DbTestCase):

    def test_created_at_defaults_to_utcnow(self):
        user = User(username='foo', email='foo@bar.com')
        user.save()
        assert_true(user.created_at)
        assert_true(isinstance(user.created_at, dt.datetime))

    def test_password_is_nullable(self):
        user = User(username='foo', email='foo@bar.com')
        user.save()
        assert_is(user.password, None)

    def test_factory(self):
        user = UserFactory(password="myprecious")
        assert_true(user.username)
        assert_true(user.email)
        assert_true(user.created_at)
        assert_false(user.is_admin)
        assert_true(user.active)
        assert_true(user.password == "myprecious")

    def test_check_password(self):
        user = User.create(username="foo", email="foo@bar.com",
                    password="foobarbaz123")
        assert_true(user.password == 'foobarbaz123')
        assert_false(user.password != "barfoobaz")

    def test_full_name(self):
        user = UserFactory(first_name="Foo", last_name="Bar")
        assert_equal(user.full_name, "Foo Bar")

    def test_roles(self):
        role = Role(name='admin')
        role.save()
        u = UserFactory()
        u.roles.append(role)
        u.save()
        assert_in(role, u.roles)

if __name__ == '__main__':
    unittest.main()