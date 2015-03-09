from django.test import TestCase
from django.test import LiveServerTestCase

from selenium.webdriver.firefox.webdriver import WebDriver

from django.test.client import Client
from django.test.client import RequestFactory

from contacts.models import Contact
from contacts.views import ListContactView
# Create your tests here.


class ContactTests(TestCase):
    def test_str(self):
        contact = Contact(first_name='John', last_name='Smith')
        self.assertEqual(
            str(contact),
            'John Smith',
        )

    def test_contacts_in_the_context(self):
        client = Client()
        response = client.get('/')
        self.assertEquals(list(response.context['object_list']), [])

        Contact.objects.create(first_name='foo', last_name='bar')
        response = client.get('/')
        self.assertEquals(response.context['object_list'].count(), 1)

    def test_contacts_in_the_context_request_factory(self):
        factory = RequestFactory()
        request = factory.get('/')

        response = ListContactView.as_view()(request)
        self.assertEquals(list(response.context_data['object_list']), [])

        Contact.objects.create(first_name='foo', last_name='bar')
        response = ListContactView.as_view()(request)
        self.assertEquals(response.context_data['object_list'].count(), 1)


class ContactListIntegrationTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(ContactListIntegrationTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(ContactListIntegrationTests, cls).tearDownClass()

    def test_contact_listed(self):
        Contact.objects.create(first_name="foo", last_name="bar")

        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        last_contact = self.selenium.find_elements_by_css_selector('.contact')[-1].find_element_by_tag_name('a')
        self.assertEqual(
            last_contact.text,
            'foo bar'
        )

    def test_contact_linked(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.assert_(
            self.selenium.find_element_by_link_text('add contact')
        )

    def test_add_contact(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.selenium.find_element_by_link_text('add contact').click()

        self.selenium.find_element_by_id('id_first_name').send_keys('test')
        self.selenium.find_element_by_id('id_last_name').send_keys('contact')
        self.selenium.find_element_by_id('id_email').send_keys('test@example.com')

        self.selenium.find_element_by_id('save_contact').click()

        last_contact = self.selenium.find_elements_by_css_selector('.contact')[-1].find_element_by_tag_name('a')

        self.assertEqual(
            last_contact.text,
            'test contact'
        )


