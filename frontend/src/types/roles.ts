export enum UserRole {
  GENERAL_MANAGER = 'GENERAL_MANAGER',
  PROJECT_MANAGER = 'PROJECT_MANAGER',
  QA_MANAGER = 'QA_MANAGER',
  LANGUAGE_REVIEWER = 'LANGUAGE_REVIEWER',
  TRANSLATOR = 'TRANSLATOR'
}

export interface RolePermissions {
  canCreateProject: boolean;
  canDeleteProject: boolean;
  canEditProject: boolean;
  canRequestDeletion: boolean;
  canApproveChanges: boolean;
  canMakeChanges: boolean;
  canManageUsers: boolean;
  canManageTerms: boolean;
  canRequestTerms: boolean;
  canAccessAdminPanel: boolean;
}

export const rolePermissions: Record<UserRole, RolePermissions> = {
  GENERAL_MANAGER: {
    canCreateProject: true,
    canDeleteProject: true,
    canEditProject: true,
    canRequestDeletion: false,
    canApproveChanges: true,
    canMakeChanges: true,
    canManageUsers: true,
    canManageTerms: true,
    canRequestTerms: false,
    canAccessAdminPanel: true
  },
  PROJECT_MANAGER: {
    canCreateProject: true,
    canDeleteProject: true,
    canEditProject: true,
    canRequestDeletion: false,
    canApproveChanges: false,
    canMakeChanges: false,
    canManageUsers: false,
    canManageTerms: false,
    canRequestTerms: true,
    canAccessAdminPanel: false
  },
  QA_MANAGER: {
    canCreateProject: true,
    canDeleteProject: false,
    canEditProject: true,
    canRequestDeletion: true,
    canApproveChanges: true,
    canMakeChanges: true,
    canManageUsers: false,
    canManageTerms: false,
    canRequestTerms: true,
    canAccessAdminPanel: false
  },
  LANGUAGE_REVIEWER: {
    canCreateProject: true,
    canDeleteProject: false,
    canEditProject: true,
    canRequestDeletion: true,
    canApproveChanges: true,
    canMakeChanges: true,
    canManageUsers: false,
    canManageTerms: false,
    canRequestTerms: true,
    canAccessAdminPanel: false
  },
  TRANSLATOR: {
    canCreateProject: true,
    canDeleteProject: false,
    canEditProject: true,
    canRequestDeletion: true,
    canApproveChanges: false,
    canMakeChanges: true,
    canManageUsers: false,
    canManageTerms: false,
    canRequestTerms: true,
    canAccessAdminPanel: false
  }
};

export function hasPermission(role: UserRole, permission: keyof RolePermissions): boolean {
  return rolePermissions[role][permission];
}

export function getUserPermissions(role: UserRole): RolePermissions {
  return rolePermissions[role];
} 