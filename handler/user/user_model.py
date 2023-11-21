class User:
    def __init__(self, id, firstName, lastName, username, profileImage, email, password, activityLevel, isDeleted, isEmailValidated, createdAt, updatedAt, userMetaInfo, socialMediaLinks, userInterests):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.profileImage = profileImage
        self.email = email
        self.password = password
        self.activityLevel = activityLevel
        self.isDeleted = isDeleted
        self.isEmailValidated = isEmailValidated
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.userMetaInfo = userMetaInfo
        self.socialMediaLinks = socialMediaLinks
        self.userInterests = userInterests
    
    def __str__(self):
        return f'''
            id: {self.id}
            firstName: {self.firstName}
            lastName: {self.lastName}
            username: {self.username}
            profileImage: {self.profileImage}
            email: {self.email}
            password: {self.password}
            activityLevel: {self.activityLevel}
            isDeleted: {self.isDeleted}
            isEmailValidated: {self.isEmailValidated}
            createdAt: {self.createdAt}
            updatedAt: {self.updatedAt}
            userMetaInfo: {self.userMetaInfo}
            socialMediaLinks: {self.socialMediaLinks}
            userInterests: {self.userInterests}
        '''
    
    
class UserMetaInfo:
    def __init__(self, id, followers, following, likes, userId):
        self.id = id
        self.followers = followers
        self.following = following
        self.likes = likes
        self.userId = userId
    
    def __str__(self):
        return f'''
            id: {self.id}
            followers: {self.followers}
            following: {self.following}
            likes: {self.likes}
            userId: {self.userId}
        '''

class SocialMediaLink:
    def __init__(self, id, icon, name, url, userId):
        self.id = id
        self.icon = icon
        self.name = name
        self.url = url
        self.userId = userId
    
    def __str__(self):
        return f'''
            id: {self.id}
            icon: {self.icon}
            name: {self.name}
            url: {self.url}
            userId: {self.userId}
        '''


class UserInterest:
    def __init__(self, userId, categoryId):
        self.userId = userId
        self.categoryId = categoryId

    def __str__(self):
        return f'''
            userId: {self.userId}
            categoryId: {self.categoryId}
        '''

class RevokedToken:
    def __init__(self, jti, revoked_at):
        self.jti = jti
        self.revoked_at = revoked_at
    
    def __str__(self):
        return f'''
            jti: {self.jti}
            revoked_at: {self.revoked_at}
        '''