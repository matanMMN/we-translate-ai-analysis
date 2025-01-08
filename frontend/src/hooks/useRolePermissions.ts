import { useSession } from 'next-auth/react';
import { UserRole, hasPermission, RolePermissions } from '@/types/roles';

export function useRolePermissions() {
  const { data: session } = useSession();
  const userRole = session?.user?.role as UserRole;

  console.log('userRole', userRole);

  const checkPermission = (permission: keyof RolePermissions): boolean => {
    if (!userRole) return false;
    return hasPermission(userRole, permission);
  };

  const checkRole = (role: UserRole): boolean => {
    return userRole === role;
  };

  return {
    userRole,
    checkPermission,
    checkRole,
    // Convenience
    isGeneralManager: userRole === UserRole.GENERAL_MANAGER,
    isProjectManager: userRole === UserRole.PROJECT_MANAGER,
    isQAManager: userRole === UserRole.QA_MANAGER,
    isLanguageReviewer: userRole === UserRole.LANGUAGE_REVIEWER,
    isTranslator: userRole === UserRole.TRANSLATOR,
  };
} 