# Skill Compare
This application uses Stack Overflows Developer Survey 2020 data to create a new dataset that contains users, their skills and other information about them.
The data is used to compare the application-user's skill and personal information with the data given from the survey. Based on that the user gets a list of similar people with their skills, salary and work-related information.
For testing-purposes there is an index.html, which delivers a list of the top20 earning users. All other data can be accessed with the api routes.:

```
/suggestions : POST

body: {
    age: 23,
    gender: 'm',
    country: 4,
    
    languages[]
        languages[0]: 'python',
        languages[1]: 'php',
        ...
}
```
```
/top : GET
```
```
/languages : GET
```
```
/countries : GET
```

---

Because the original dataset is too large to upload to the repository, the aggregated csv has been saved instead.
The function for creating the dataset from the survey csv is: aggregate_csv_data (create_csv.py)

## Project setup
`docker build -t python-skill-compare .`

`docker run -p 5000:5000 -it python-skill-compare`

## Dependencies
`CurrencyConverter 0.14.4`
`Flask >= 1.1.2`
`Flask-Cors >= 3.0.9`
`matplotlib >= 3.3.3`
`numpy 1.19.5`
`pandas >= 1.2.0`

## Resources

### initial used dataset
[Stack Overflow Developer Survey 2020](https://insights.stackoverflow.com/survey)
