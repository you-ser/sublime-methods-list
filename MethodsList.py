import sublime
import sublime_plugin

import re

class MethodsListCommand(sublime_plugin.WindowCommand):

	def run(self):
		if not self.get_view():
			return

		self.create_modules_list()
		content = list(map(lambda module: [module['name'], module['params']], self.modules_list))
		if len(content) < 1:
			content.append('Nothing found')

		self.window.show_quick_panel(content, self.on_done)

	def on_done(self, index):

		if index < 0 or index > len(self.modules_list) -1:
			return

		line, _col = self.get_view().rowcol(self.modules_list[index]['point'].begin())
		self.get_view().run_command("goto_line", {"line": line + 1})

	def get_view(self):
		return self.window.active_view()

	def create_modules_list(self):
		self.modules_list = []
		for point in self.search_modules_list():
			definition = self.parse_module_definition(point)
			if len(definition):
				self.modules_list.append(definition)

	def search_modules_list(self):
		return self.get_view().find_all('(public|private|protected)?\s+function.*?\)')

	def parse_module_definition(self, point):
		line = self.get_view().substr(self.get_view().line(point))
		m = re.search(r".*(?P<visibility>public|protected|private)?\s+function\s+(?P<name>\w+)\s*(?P<params>\(.*?\))", line)

		if not m:
			return {}

		params = m.groupdict()
		if not params.get('visibility'):
			params['visibility'] = 'public'

		params['point'] = point
		params['description'] = '{name} {visibility} {params}'.format(**params)

		return params

