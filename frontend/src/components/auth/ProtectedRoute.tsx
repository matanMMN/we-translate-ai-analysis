import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { ReactNode, useEffect } from 'react';
import { UserRole, hasPermission, RolePermissions } from '@/types/roles';
import LoadingSpinner from '../LoadingSpinner';

interface ProtectedRouteProps {
  children: ReactNode;
  requiredRole?: UserRole;
  requiredPermission?: keyof RolePermissions;
}

export function ProtectedRoute({ 
  children, 
  requiredRole, 
  requiredPermission 
}: ProtectedRouteProps) {
  const { data: session, status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (status === 'loading') return;

    if (!session) {
      router.push('/login');
      return;
    }

    const userRole = session.user.role as UserRole;

    if (requiredRole && userRole !== requiredRole) {
      router.push('/unauthorized');
      return;
    }

    if (requiredPermission && !hasPermission(userRole, requiredPermission)) {
      router.push('/unauthorized');
      return;
    }
  }, [session, status, requiredRole, requiredPermission, router]);

  if (status === 'loading') {
    return <LoadingSpinner />;
  }

  return <>{children}</>;
} 