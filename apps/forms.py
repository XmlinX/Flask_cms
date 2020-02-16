from wtforms import Form


class BaseForm(Form):

    def get_errors(self):
        errors = self.errors
        message = errors.popitem()[1][0]
        return message