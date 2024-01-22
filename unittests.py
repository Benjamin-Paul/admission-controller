import unittest
from flask_testing import TestCase
from server import app
import json

class TestServer(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_validate(self):
        # Test case where "kubernetes.io/change-cause" is not in annotations
        response = self.client.post("/validate", data=json.dumps({
            "request": {
                "uid": "test_uid",
                "object": {
                    "metadata": {
                        "annotations": {}
                    }
                }
            }
        }), content_type='application/json')
        self.assertEqual(response.json["response"]["allowed"], False)
        self.assertEqual(response.json["response"]["status"]["message"], "kubernetes.io/change-cause is mandatory for deployments in this namespace.")

        # Test case where oldObject is None
        response = self.client.post("/validate", data=json.dumps({
            "request": {
                "uid": "test_uid",
                "object": {
                    "metadata": {
                        "annotations": {
                            "kubernetes.io/change-cause": "test_change_cause"
                        }
                    }
                },
                "oldObject": None
            }
        }), content_type='application/json')
        self.assertEqual(response.json["response"]["status"]["message"], "Ok. First change-cause provided.")

        # Test case where "kubernetes.io/change-cause" is unchanged
        response = self.client.post("/validate", data=json.dumps({
            "request": {
                "uid": "test_uid",
                "object": {
                    "metadata": {
                        "annotations": {
                            "kubernetes.io/change-cause": "test_change_cause"
                        }
                    }
                },
                "oldObject": {
                    "metadata": {
                        "annotations": {
                            "kubernetes.io/change-cause": "test_change_cause"
                        }
                    }
                }
            }
        }), content_type='application/json')
        self.assertEqual(response.json["response"]["allowed"], False)
        self.assertEqual(response.json["response"]["status"]["message"], "kubernetes.io/change-cause unchanged. You must modify it.")

        # Test case where KeyError is raised
        response = self.client.post("/validate", data=json.dumps({
            "request": {
                "uid": "test_uid",
                "object": {}
            }
        }), content_type='application/json')
        self.assertEqual(response.json["response"]["allowed"], False)
        self.assertEqual(response.json["response"]["status"]["message"], "Inernal error. Reach out to the developper : https://github.com/Benjamin-Paul")

if __name__ == '__main__':
    unittest.main()