from celery import Celery

def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config['CELERY_CONFIG'])
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        # abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run( *args, **kwargs)
            
    celery.Task = ContextTask

    return celery
