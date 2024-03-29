import os
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from prometheus_flask_exporter import PrometheusMetrics
from flask import Blueprint, request
from flask_restplus import Api


from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)

metrics = PrometheusMetrics(blueprint)

@blueprint.route('/metrics')
def meter():
  from prometheus_client import multiprocess, CollectorRegistry

  if 'prometheus_multiproc_dir' in os.environ:
      registry = CollectorRegistry()
  else:
      registry = metrics.registry

  if 'name[]' in request.args:
      registry = registry.restricted_registry(request.args.getlist('name[]'))

  if 'prometheus_multiproc_dir' in os.environ:
      multiprocess.MultiProcessCollector(registry)
      
  headers = {'Content-Type': CONTENT_TYPE_LATEST}
  return generate_latest(registry), 200, headers
