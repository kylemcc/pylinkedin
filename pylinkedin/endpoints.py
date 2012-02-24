BASE_API = "https://api.linkedin.com/v1/"

"""
Groups resources
Documentation: http://developer.linkedin.com/documents/groups
"""

GROUP_MEMBERSHIPS = BASE_API + "people/~/group-memberships:(group:(id,name,short-description,description,category,website-url,site-group-url,large-logo-url,num-members),membership-state,show-group-logo-in-profile,allow-messages-from-members,email-digest-frequency,email-announcements-from-managers,email-for-every-new-post)"


"""
Social Stream resources
Documentation: http://developer.linkedin.com/documents/social-stream
"""

NETWORK_UPDATES = BASE_API + "people/~/network/updates"