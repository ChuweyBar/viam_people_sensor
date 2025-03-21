# Module sensor 

This module houses the people_sensor model.

## Model cwb:sensor:people_sensor

This is a sensor component that depends on a camera component and a vision service.
It detects any configured label using the vision service from the camera.
Provide a description of the model and any relevant information.

### Configuration
The following attribute template can be used to configure this model:

```json
{
"label": <string>,
"camera_name": <string>
}
```

#### Attributes

The following attributes are available for this model:

| Name          | Type   | Inclusion | Description                |
|---------------|--------|-----------|----------------------------|
| `label` | string  | Required  | Name of label to detect from vision service |
| `camera_name` | string | Required  | Name of camera to be used by vision service |

#### Example Configuration

```json
{
  "label": "Person",
  "camera_name": "camera_1"
}
```
