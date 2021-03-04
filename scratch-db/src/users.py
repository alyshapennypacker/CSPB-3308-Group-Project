class User:
    def __init__(self, profileId, profilePic):
        self.profileId = profileId
        self.profilePic = profilePic
        self.interests = self.selectInterests()

    def __str__(self):
        return self.firstName + " " + self.lastName

    def setProile(self):
        '''
        GET data from application form
        '''
        def personalInfo() -> None:
            ''' GET from personal info form '''
            self.firstName = None
            self.lastName = None
            self.email = None
            self.email = None

        def projectTopics(self) -> list:
            ''' GET from project topics form '''
            self.projectTopics = []


if __name__ == '__main__':
    user1 = User(1, "dan", "bae", "dan.bae@email.edu")
    print(user1)
