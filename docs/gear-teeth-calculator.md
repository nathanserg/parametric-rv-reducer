# Gear teeth calculator

## Goal
The gear teeth calculator is meant to:
- calculate the number of teeth per sun and planets to fit inside the cycloidal disk
- calculate the cutout diameter inside the cycloidal disk
- get round number as reduction ratio for easier calculation in software

## Example
Parameters:  
![parameters example](docs/pictures/parameters-example.png)

Result:  
![result example](docs/pictures/result-example.png)

Result if gear ratio of 1:1 are filtered out:  
`unit_gear_ratio` change to False  
![result example without 1:1](docs/pictures/result-example-unit.png)

Result if filtered by exact modulus:  
`filter_by_given_modulus` change to True  
![result example with exact modulus](docs/pictures/result-given-modulus.png)

