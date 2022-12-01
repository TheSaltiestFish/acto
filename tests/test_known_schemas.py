import sys
import unittest
import yaml

sys.path.append('..')
sys.path.append('.')

from known_schemas import *
from schema import extract_schema


class TestSchema(unittest.TestCase):

    def test_statefulset_match(self):
        with open('rabbitmq_crd.yaml', 'r') as operator_yaml:
            crd = yaml.load(operator_yaml, Loader=yaml.FullLoader)
            spec_schema = ObjectSchema(
                ['root'], crd['spec']['versions'][0]['schema']['openAPIV3Schema']['properties']
                ['spec']['properties']['override']['properties']['statefulSet'])

        self.assertTrue(StatefulSetSchema.Match(spec_schema))

    def test_service_match(self):
        with open('rabbitmq_crd.yaml', 'r') as operator_yaml:
            crd = yaml.load(operator_yaml, Loader=yaml.FullLoader)
            spec_schema = ObjectSchema(
                ['root'], crd['spec']['versions'][0]['schema']['openAPIV3Schema']['properties']
                ['spec']['properties']['override']['properties']['service'])

        self.assertTrue(ServiceSchema.Match(spec_schema))

    def test_affinity_match(self):
        with open('rabbitmq_crd.yaml', 'r') as operator_yaml:
            crd = yaml.load(operator_yaml, Loader=yaml.FullLoader)
            spec_schema = ObjectSchema(['root'],
                                       crd['spec']['versions'][0]['schema']['openAPIV3Schema']
                                       ['properties']['spec']['properties']['affinity'])

        self.assertTrue(AffinitySchema.Match(spec_schema))

    def test_tolerations_match(self):
        with open('rabbitmq_crd.yaml', 'r') as operator_yaml:
            crd = yaml.load(operator_yaml, Loader=yaml.FullLoader)
            spec_schema = ArraySchema(['root'],
                                      crd['spec']['versions'][0]['schema']['openAPIV3Schema']
                                      ['properties']['spec']['properties']['tolerations'])

        self.assertTrue(TolerationsSchema.Match(spec_schema))

    def test_tolerations_not_match(self):
        with open('rabbitmq_crd.yaml', 'r') as operator_yaml:
            crd = yaml.load(operator_yaml, Loader=yaml.FullLoader)
            spec_schema = ObjectSchema(['root'],
                                       crd['spec']['versions'][0]['schema']['openAPIV3Schema']
                                       ['properties']['spec']['properties']['tolerations']['items'])

        self.assertFalse(TolerationsSchema.Match(spec_schema))

    def test_resources_match(self):
        with open('rabbitmq_crd.yaml', 'r') as operator_yaml:
            crd = yaml.load(operator_yaml, Loader=yaml.FullLoader)
            spec_schema = ObjectSchema(['root'],
                                       crd['spec']['versions'][0]['schema']['openAPIV3Schema']
                                       ['properties']['spec']['properties']['resources'])

        self.assertTrue(ResourceRequirementsSchema.Match(spec_schema))

    def test_container_match(self):
        with open('rabbitmq_crd.yaml', 'r') as operator_yaml:
            crd = yaml.load(operator_yaml, Loader=yaml.FullLoader)
            spec_schema = ObjectSchema(
                ['root'], crd['spec']['versions'][0]['schema']['openAPIV3Schema']['properties']
                ['spec']['properties']['override']['properties']['statefulSet']['properties']
                ['spec']['properties']['template']['properties']['spec']['properties']['containers']['items'])

        self.assertTrue(ContainerSchema.Match(spec_schema))

        with open('psmdb.percona.com_perconaservermongodbs.yaml', 'r') as operator_yaml:
            crd = yaml.load(operator_yaml, Loader=yaml.FullLoader)
            spec_schema = ObjectSchema(
                ['root'], crd['spec']['versions'][-1]['schema']['openAPIV3Schema']['properties']
                ['spec']['properties']['replsets']['items']['properties']['sidecars']['items'])

        self.assertTrue(ContainerSchema.Match(spec_schema))

    def test_find_matches(self):
        with open('rabbitmq_crd.yaml', 'r') as operator_yaml:
            crd = yaml.load(operator_yaml, Loader=yaml.FullLoader)
            spec_schema = extract_schema([],
                                         crd['spec']['versions'][0]['schema']['openAPIV3Schema'])
            print(find_all_matched_schemas(spec_schema))


if __name__ == '__main__':
    unittest.main()