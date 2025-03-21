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
"label": <string>
}
```

Note this sensor also requires the following as dependencies:
- 1 x camera component
- 1 x vision service

#### Attributes

The following attributes are available for this model:

| Name          | Type   | Inclusion | Description                |
|---------------|--------|-----------|----------------------------|
| `label` | string  | Optional  | Name of label to detect from vision service, default to 'Person' |

#### Example Configuration

```json
{
  "label": "Chair"
}
```
