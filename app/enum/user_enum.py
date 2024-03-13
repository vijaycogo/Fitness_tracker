from enum import Enum as UserEnum

#Defining enumeration for use and admin roles.
class UserRole(UserEnum):
    admin = "admin"
    customer = "customer"

    