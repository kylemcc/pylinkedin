BASE_API = "https://api.linkedin.com/v1/"

"""
Groups resources
Documentation: http://developer.linkedin.com/documents/groups
"""

GROUP_MEMBERSHIPS = BASE_API + "people/~/group-memberships:(group:(id,name,short-description,description,category,website-url,site-group-url,large-logo-url,num-members),membership-state,show-group-logo-in-profile,allow-messages-from-members,email-digest-frequency,email-announcements-from-managers,email-for-every-new-post)"
GROUP_FEED = BASE_API + "groups/{group_id}/posts:(id,creation-timestamp,title,summary,creator:(id,first-name,last-name,picture-url,headline),likes,attachment:(image-url,content-domain,content-url,title,summary),relation-to-viewer)"


"""
Social Stream resources
Documentation: http://developer.linkedin.com/documents/social-stream
"""

NETWORK_UPDATES = BASE_API + "people/~/network/updates"