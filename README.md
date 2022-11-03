# deanslist

## Getting started

1. Ensure you have Python 3.6+ installed
2. Create and activate a virtual environment
3. Fork of this repository
4. Install `requirements.txt`
5. Edit the `endpoint_queries` variable in `settings.py` with your desired endpoints and parameters
6. Create a `JSON` file containing your API credentials in an array of objects, like so:

   ```json
   [
       {
           "school-name": "myschool",
           "region-name": "myschoolsregion",
           "key": "tH15iSmYD3@n51157k3y"
       },
       ...
   ]
   ```

7. Create a `.env` file containing the following variables:

   ```env
   CURRENT_ACADEMIC_YEAR=20XX
   FIRST_ACADEMIC_YEAR=20XX
   INSTANCE_NAME=myinstancename
   LOCAL_TIMEZONE=CNTRY/TZ
   GCS_BUCKET_NAME=my-bucket-name
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/gcs-creds.json
   DEANSLIST_APPLICATION_CREDENTIALS=/path/to/api-keys.json
   ```
