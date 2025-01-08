import { NextResponse } from 'next/server';
import { getSession } from '@/lib/AuthGuard';
import { RolePermissions, UserRole, hasPermission } from '@/types/roles';

export type PermissionRequirement = {
  requiredRole?: UserRole;
  requiredPermission?: keyof RolePermissions;
}

export async function withRoleProtection(
  handler: Function, 
  { requiredRole, requiredPermission }: PermissionRequirement
) {
  return async (...args: any[]) => {
    const session = await getSession();

    if (!session?.user) {
      return NextResponse.redirect(new URL('/login', process.env.NEXTAUTH_URL));
    }

    const userRole = session.user.role as UserRole;

    if (requiredRole && userRole !== requiredRole) {
      return NextResponse.json(
        { error: 'Insufficient permissions' },
        { status: 403 }
      );
    }

    if (requiredPermission && !hasPermission(userRole, requiredPermission)) {
      return NextResponse.json(
        { error: 'Insufficient permissions' },
        { status: 403 }
      );
    }

    return handler(...args);
  };
} 