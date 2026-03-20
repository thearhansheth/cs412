# File: voter_analytics/models.py
# Author: Arhan Sheth, 3/20/2026
# Email: aksheth@bu.edu
# Description: models.py for Voter Analytics


from django.db import models
import datetime
import csv

# Create your models here.
class Voter(models.Model):
    """Store the data from one voter in the town of Newton, MA
    """

    # Identification & Address
    voter_id = models.TextField()
    last_name = models.TextField()
    first_name = models.TextField()
    street_num = models.IntegerField(null=True, blank=True)     # nullable in case of missing data
    street_name = models.TextField()
    apt_num = models.CharField(max_length=10, null=True, blank=True)
    zip = models.CharField(max_length=10)
    dob = models.DateField(null=True, blank=True)
    date_registration = models.DateField(null=True, blank=True)
    party = models.CharField(max_length=2, null=True, blank=True)       # 2-char field, e.g. 'D ', 'R ', 'U '
    precinct = models.CharField(max_length=10, null=True, blank=True)

    # Election Participation
    v20 = models.BooleanField(null=True, blank=True)
    v21town = models.BooleanField(null=True, blank=True)
    v21primary = models.BooleanField(null=True, blank=True)
    v22 = models.BooleanField(null=True, blank=True)
    v23 = models.BooleanField(null=True, blank=True)

    voter_score = models.IntegerField()


    def __str__(self):
        """Returns a string representation of the model instance.
        """
        return f'{self.first_name} {self.last_name} ({self.voter_id}, {self.dob}), {self.voter_score}'



def load_data():
    """Loads data records from CSV file into Django model instances.
    """

    filename = 'voter_analytics/newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers
    
    for line in f:
        fields = line.split(',')
        try:
            # helper to convert 'TRUE'/'FALSE' strings to Python booleans
            def parse_bool(x):
                return x.strip().upper() == 'TRUE'

            voter = Voter(
                voter_id=fields[0],
                last_name=fields[1],
                first_name=fields[2],
                street_num=int(fields[3]),
                street_name=fields[4],
                apt_num=fields[5],
                zip=fields[6],
                dob=fields[7],
                date_registration=fields[8],
                party=fields[9].strip(),        # strip trailing space from 1-char party codes
                precinct=fields[10],
                v20=parse_bool(fields[11]),
                v21town=parse_bool(fields[12]),
                v21primary=parse_bool(fields[13]),
                v22=parse_bool(fields[14]),
                v23=parse_bool(fields[15]),
                voter_score=int(fields[16])
            )

            voter.save()
            print(f"Created voter: {voter}")

        except:
            # skip rows with missing or malformed fields
            print(f"Skipped: {fields}")

    print(f"Done. Created {Voter.objects.count()} voters.")