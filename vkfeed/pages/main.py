# -*- coding: utf-8 -*-

'''Generates the main page.'''

import re
import urllib

import webapp2

import vkfeed.util


class MainPage(webapp2.RequestHandler):
    '''Generates the main page.'''


    def get(self):
        '''Processes a GET request.'''

        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        self.response.out.write(vkfeed.util.render_template('main.html', {
            'show_like_buttons': True }))


    def post(self):
        '''Processes a POST request.'''

        profile_url = self.request.get('profile_url', '')

        match = re.match(r'''^
            \s*
            (?:https?://(?:www\.)?(?:vk\.com|vkontakte\.ru)/)?
            (?P<profile_id>[a-zA-Z0-9._-]+)/?
            \s*
        $''', profile_url, re.IGNORECASE | re.VERBOSE)

        if match:
            params = {}

            if self.request.get('foreign_posts') == '1':
                params['foreign_posts'] = '1'

            if self.request.get('show_photo') != '1':
                params['show_photo'] = '0'

            params = '?' + urllib.urlencode(params) if params else ''

            self.redirect('/feed/' + match.group('profile_id') + '/wall' + params)
        else:
            self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
            self.response.out.write(vkfeed.util.render_template('main.html', {
                'post_error': u'''
                    Неверно указан URL профиля.
                    Адрес должен быть вида http://vkontakte.ru/имя_профиля.
                    Имя профиля должно удовлетворять требованиям, предъявляемым администрацией ВКонтакте.
                ''',
                'show_like_buttons': True,
            }))

