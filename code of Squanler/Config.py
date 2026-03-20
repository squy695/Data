import time

def getNowTime():
    return int(round(time.time()))

class Config:
    def __init__(self):
        
        # You can enhance the cycles configuration by adding additional status codes that may be relevant to your application's entry interfaces.
        # For now, we only consider these three status codes
        self.cycles = ['2..', '302', '5..']
        
        # The namespace of your application.
        self.namespace = 'hipster'
        # The namespace of your cluster's entry point (typically istio-ingressgateway).
        self.ingress_namespace = 'istio-system'
        # The name of your cluster's entry point.
        self.ingress = 'istio-ingressgateway'
        
        # The call chain relationships between your application's entry interfaces (parent -> child).
        self.redict_chain = [
            ['/setCurrency && POST', '/ && GET'],
        ]

        # The target end-to-end latency.
        self.SLO = 200
        # The execution interval.
        self.scale_interval = 30
        # The CPU request for the service.
        self.request = 150

        # The services.
        self.svcs = ['frontend','adservice','cartservice','checkoutservice','currencyservice','emailservice','paymentservice','productcatalogservice','recommendationservice','shippingservice']
        
        # your CCpR matrix.
        self.interfaces = {
            "/ && GET": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], self.SLO],
            "/product/{id} && GET": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], self.SLO],
            '/cart && GET': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], self.SLO],
            '/cart/checkout && POST': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], self.SLO],
            '/setCurrency && POST': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], self.SLO],
        }

        # the maximum and minimum allowable instance count.
        self.max_pod = 100
        self.min_pod = 1

        # the duration of the experiment.
        self.duration = 1 * 60 * 60
        self.start = getNowTime()
        self.end = self.start + self.duration
        self.step = 5

        # The address of your Prometheus instance.
        self.prom_range_url = "http://XXX.XXX.XX.XXX:XXXXX//api/v1/query_range"
        self.prom_no_range_url = "http://XXX.XXX.XX.XXX:XXXXX//api/v1/query"