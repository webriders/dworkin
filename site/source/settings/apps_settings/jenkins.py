
PROJECT_APPS = ('techblog',)

JENKINS_TASKS = ('django_jenkins.tasks.run_pylint',
                 'django_jenkins.tasks.run_pep8',
                 #'django_jenkins.tasks.run_pyflakes',
                 'django_jenkins.tasks.with_coverage',
                 'django_jenkins.tasks.django_tests',)