from typing import (Any, ClassVar, Dict, Final, List, Mapping, Optional,
                    Sequence)

from typing_extensions import Self
from viam.components.sensor import *
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import Geometry, ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.utils import SensorReading, ValueTypes, struct_to_dict

#from viam.logging import getLogger

from viam.services.vision.client import VisionClient
from viam.components.camera.client import CameraClient

#log = getLogger(__name__)

class PeopleSensor(Sensor, EasyResource):
    # To enable debug-level logging, either run viam-server with the --debug option,
    # or configure your resource/machine to display debug logs.
    MODEL: ClassVar[Model] = Model(ModelFamily("cwb", "people_sensor"), "people_sensor")

    _configFields: Dict
    _label: str
    _visionClient: VisionClient = None
    _cameraClient: CameraClient = None

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        """This method creates a new instance of this Sensor component.
        The default implementation sets the name from the `config` parameter and then calls `reconfigure`.

        Args:
            config (ComponentConfig): The configuration for this resource
            dependencies (Mapping[ResourceName, ResourceBase]): The dependencies (both implicit and explicit)

        Returns:
            Self: The resource
        """
        return super().new(config, dependencies)

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        """This method allows you to validate the configuration object received from the machine,
        as well as to return any implicit dependencies based on that `config`.

        Args:
            config (ComponentConfig): The configuration for this resource

        Returns:
            Sequence[str]: A list of implicit dependencies
        """
        """
        fields = struct_to_dict(config.attributes)
        label = fields.get('label')
        if label is None:
            raise Exception("Config must specify 'label' field for sensor to detect.")
        """
        return []

    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        """This method allows you to dynamically update your service when it receives a new `config` object.

        Args:
            config (ComponentConfig): The new configuration
            dependencies (Mapping[ResourceName, ResourceBase]): Any dependencies (both implicit and explicit)
        """

        self._configFields = struct_to_dict(config.attributes)
        clients = list(dependencies.values())

        # given validate_config this should be safe
        self._label = self._configFields.get('label', 'Person')
        self.logger.debug('Detecting label %r', self._label)

        if len(clients) != 2:
            raise Exception('This component requires a camera component and a vision service as dependency to function.')
        for client in clients:
            if isinstance(client, VisionClient):
                self._visionClient = client
            elif isinstance(client, CameraClient):
                self._cameraClient = client
            else:
                raise Exception('Found dependency %r, which is neither a VisionClient nor a CameraClient', client)
        if self._visionClient is None:
            raise Exception('Did not find vision in dependency')
        if self._cameraClient is None:
            raise Exception('Did not find camera in dependency')

        return super().reconfigure(config, dependencies)

    async def get_readings(
        self,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, SensorReading]:
        """
        self._dependencies[Vision.get_resource_name()]
        peopleDetector = Vision.get_resource_name(visionServiceName)
        assert isinstance(peopleDetector, Vision)
        """

        image = await self._cameraClient.get_image()
        detections = await self._visionClient.get_detections(image)
        labelString = self._label.lower() + "_detected"
        for detection in detections:
            if detection.class_name == self._label:
                return {
                    labelString: 1
                }
        return {
            labelString: 0
        }
        

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        self.logger.error("`do_command` is not implemented")
        raise NotImplementedError()

    async def get_geometries(
        self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None
    ) -> List[Geometry]:
        self.logger.error("`get_geometries` is not implemented")
        raise NotImplementedError()

