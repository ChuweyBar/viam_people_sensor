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

from viam.logging import getLogger

from viam.services.vision import Vision, VisionClient

from viam.services.vision import Detection

LOGGER = getLogger(__name__)

class PeopleSensor(Sensor, EasyResource):
    # To enable debug-level logging, either run viam-server with the --debug option,
    # or configure your resource/machine to display debug logs.
    MODEL: ClassVar[Model] = Model(ModelFamily("cwb", "people_sensor"), "people_sensor")

    _configFields: Dict
    _label: str
    _visionClient: VisionClient
    _cameraName: str

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
        fields = struct_to_dict(config.attributes)
        label = fields.get('label', None)
        if label is None:
            raise Exception("Config must specify 'label' field for sensor to detect.")

        cameraName = fields.get('camera_name', None)
        if cameraName is None:
            raise Exception("Config must specify 'camera_name' for sensor to detect.")

        # need to have dependency on vision service
        return []

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        """This method allows you to dynamically update your service when it receives a new `config` object.

        Args:
            config (ComponentConfig): The new configuration
            dependencies (Mapping[ResourceName, ResourceBase]): Any dependencies (both implicit and explicit)
        """
        self._configFields = struct_to_dict(config.attributes)

        # given validate_config this should be safe
        self._label = self._configFields['label']
        self.logger.debug('Detecting label %r', self._label)

        self._cameraName = self._configFields['camera_name']
        self.logger.debug('Detecting via camera %r', self._cameraName)

        visionClients = list(dependencies.values())
        # hardcoding, should easily support multiple visionClients
        if len(visionClients) > 1:
            raise Exception("Currently does not support more than 1 dependency.")
        if len(visionClients) < 1:
            raise Exception("For sensor to function properly, please add a vision/mlmodel service as dependency.")
        self._visionClient = visionClients[0]
        LOGGER.info('self._visionClient %r', self._visionClient)
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

        detections = await self._visionClient.get_detections_from_camera(camera_name=self._cameraName)
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

