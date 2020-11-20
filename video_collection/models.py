from urllib import parse 
from django.db import models
from django.core.exceptions import ValidationError

class Video(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    notes = models.TextField(blank=True, null=True)
    video_id = models.CharField(max_length=40, unique=True)

    def save(self, *args, **kwargs):
        # checks for a valid YouTube URL in the form
        # https://www.youtube.com/watch?v=12345678
        # where 12345678 is the video ID
        # extract the video id from the URL, prevent save if not valid YouTube URL or id ID is not found in URL
        try:
            url_components = parse.urlparse(self.url)

            if url_components.scheme != 'https':
                raise ValidationError(f'Not a YouTube URL {self.url}')

            if url_components.netloc != 'www.youtube.com':
                raise ValidationError(f'Not a YouTube URL {self.url}')
                
            if url_components.path != '/watch':
                raise ValidationError(f'Not a YouTube URL {self.url}')
            
            query_string = url_components.query
            if not query_string:
                raise ValidationError(f'Invalid YouTube URL {self.url}')
            parameters = parse.parse_qs(query_string, strict_parsing=True)
            parameter_list = parameters.get('v')
            if not parameter_list:   # empty string, empty list... 
                raise ValidationError(f'Invalid YouTube URL parameters {self.url}')
            self.video_id = parameter_list[0]   # set the video ID for this Video object 
        except ValueError as e:   # URL parsing errors, malformed URLs
            raise ValidationError(f'Unable to parse URL {self.url}') from e

        super().save(*args, **kwargs)  # don't forget!
                    

    def __str__(self):
        # String displayed in the admin console, or when printing a model object. 
        # You can return any useful string here. Optionally 
        if not self.notes:
            notes = 'No notes'
        else:
            notes = self.notes[:200]
        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url},  \
        Video ID: {self.video_id},  Notes: {notes}'
