import logging
import os
import time

from flask import Flask, request
from jaeger_client import Config
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
metrics = PrometheusMetrics(app)


config = Config(
    config={
        'local_agent': {
                'reporting_host': 'simplest-agent.default.svc.cluster.local', 
                'reporting_port': '6831',
        },
        'logging': True,
    },
    service_name='myapp',
)
tracer = config.initialize_tracer()


metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)


@app.route('/handler')
def handler():
    with tracer.start_span('HttpReq') as span:
        with tracer.start_span('CollectInfo', child_of=span) as child_span:
            time.sleep(0.1)

        with tracer.start_span('DatabaseRequest', child_of=span) as child_span:
            time.sleep(0.03)
        return 'OK'


if __name__ == '__main__':
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    app.run(host='0.0.0.0', port=os.getenv("HTTP_PORT", 8081))
