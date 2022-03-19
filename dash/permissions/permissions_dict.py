PERMISSIONS = [
    {
        "permission_name":"attendance",
        "role_name":"Attendance Manager",
        
    },
    {
        "permission_name":"parent",
        "role_name":"Parent",
    },
    {
        "permission_name":"big_daddy",
        "role_name":"Master Platform",
    },    
]

def create_perms_list():
    permissions_list = []
    for permission in PERMISSIONS:
        perm_tuple = []
        for v in permission.values():
            perm_tuple.append(v)
        permissions_list.append(tuple(perm_tuple))
    return permissions_list