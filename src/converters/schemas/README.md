# Data Model

This document outlines a data model represented in JSON Schema format.

## Definitions

### Atomic Model

- Type: `string`
- Enum: ["Point", "Sphere", "Gaussian"]

### Data Class

- Type: `string`
- Enum: ["Sim", "Synth", "Exp"]

### Domain

- Type: `string`
- Enum: ["Real", "Frequency"]

### Data Type

- Type: `string`
- Enum: ["Image", "Filter", "Other"]

### Point (DataModel_P)

- Type: `object`
- Description: Point Coordinate in R3
- Properties:
  - `x`: `number`
  - `y`: `number`
  - `z`: `number`

### Quaternion (DataModel_Quaternion)

- Type: `object`
- Description: Quaternion h = a + bi + cj + dk
- Properties:
  - `a`: `number`
  - `b`: `number`
  - `c`: `number`
  - `d`: `number`

### Atom (DataModel_Atom)

- Type: `object`
- Description: Atom
- Properties:
  - `pos`: [DataModel_P](#point-datamodel_p)
  - `mass`: `number`
  - `name`: `number`
  - `model`: [DataModel_AtomicModel](#atomic-model)

### Structure (DataModel_Structure)

- Type: `object`
- Description: A group of associated atoms corresponding to a conformation with at least one (implicit) orientation
- Properties:
  - `atoms`: Array of [DataModel_Atom](#atom-datamodel_atom)
  - `orientations`: Array of [DataModel_Quaternion](#quaternion-datamodel_quaternion)

### Constant Table (DataModel_ConstantTable)

- Type: `object`
- Description: Table for looking up constants
- Properties:
  - `amplitude`: `boolean`
  - `defocus`: `boolean`
  - `b_factor`: `boolean`
  - `img_dims`: `boolean`
  - `num_pixels`: `boolean`
  - `pixel_width`: `boolean`
  - `elecwavel`: `boolean`
  - `snr`: `boolean`
  - `experiment_parameters`: `boolean`
  - `seed`: `boolean`
  - `structures`: `boolean`
  - `coordinates`: `boolean`

### Parameters (DataModel_Parameters)

- Type: `object`
- Properties:
  - `amplitude`: Array of `number`
  - `defocus`: Array of `number`
  - `b_factor`: Array of `number`
  - `img_dims`: Array of `number`
  - `num_pixels`: Array of `number`
  - `pixel_width`: Array of `number`
  - `sigma`: Array of `number`
  - `elecwavel`: Array of `number`
  - `snr`: Array of `number`
  - `experiment_parameters`: Array of `number`
  - `seed`: Array of `number`
  - `structures`: Array of `number`
  - `coordinates`: Array of `number`

### Matrix (DataModel_Matrix)

- Type: `object`
- Description: Could be an image or a filter
- Properties:
  - `real_pixels`: Array of `number`
  - `imag_pixels`: Array of `number`
  - `orientation_id`: `number`
  - `data_type`: [DataModel_DataType](#data-type)
  - `data_space`: [DataModel_Domain](#domain)
  - `parent_structure`: `number`

### Datum (DataModel_Datum)

- Type: `object`
- Description: An object of a dataset to be used by processes which interact with DataSets
- Properties:
  - `m1`: [DataModel_Matrix](#matrix-datamodel_matrix)
  - `m2`: [DataModel_Matrix](#matrix-datamodel_matrix)
  - `param_id`: `number`

### DataSet (DataModel_DataSet)

- Type: `object`
- Properties:
  - `data`: Array of [DataModel_Datum](#datum-datamodel_datum)
  - `params`: [DataModel_Parameters](#parameters-datamodel_parameters)
