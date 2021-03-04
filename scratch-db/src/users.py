class User:
    def __init__(self, profileId):
        self.profileId = profileId
        self.friends = []
        self.projects = []
        self.communitiesFollowed = {
            'communities': [],
            'isAdmin': False  # Ability to post projects
        }

    def __str__(self):
        return self.firstName + " " + self.lastName

    def getProile(self):
        '''
        GET data from 3-step application form
        '''

        def getPersonalInfo(self):
            ''' GET from personalInfo form '''
            self.profileInfo = {
                'firstName': None,
                'lastName': None,
                'email': None,
            }
            self.profilePic = None

        # Based off stackoverflow objects, see in ../meta/stackoverflow_survey_data.py
        # Restrict selection (i.e. pick up to X topics)
        def getProjectTopics(self):
            ''' GET from projectTopics form '''
            self.interests = {
                'industry': [],
                'roles': [],
                'technologies': {
                    'profficient': [],
                    'wantToLearn': []
                }
            }

        def getConstraints(self):
            ''' GET from contraints form '''
            self.constraints = {
                self.weeklyTimeCommit: None,  # format: Hours/week
                self.yearsOfExp: None,
                self.numProjects: None,
            }

    def saveProfile(self):
        '''
        Save user info in .db file
        '''
        pass


if __name__ == '__main__':
    user1 = User(1, "dan", "bae", "dan.bae@email.edu")
    print(user1)
