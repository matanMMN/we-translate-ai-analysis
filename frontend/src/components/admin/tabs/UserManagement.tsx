'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { getAllUsers, updateUserRole } from '@/actions/getAllUsers'
import { Dialog, DialogTitle } from '@headlessui/react'
import { format } from 'date-fns'
import { User } from '@/lib/userData'
import { UserRole } from '@/types/roles'
import { ChevronDownIcon, ChevronLeftIcon } from '@heroicons/react/24/outline'

const USER_ROLES = Object.values(UserRole).filter(role => role !== "GENERAL_MANAGER").map(role => {
    return role.charAt(0).toUpperCase() + role.slice(1).toLowerCase().replace(/_/g, ' ')
})
        
console.log(USER_ROLES)

type RoleChangeConfirmation = {
  isOpen: boolean
  user: User | null
  newRole: UserRole | null
}

export function UserManagement() {
  const [users, setUsers] = useState<User[]>([])
  const [roleChangeConfirm, setRoleChangeConfirm] = useState<RoleChangeConfirmation>({
    isOpen: false,
    user: null,
    newRole: null
  })

  useEffect(() => {
    loadUsers()
  }, [])

  const loadUsers = async () => {
    try {
      const data = await getAllUsers()
      setUsers(data)
    } catch (error) {
      console.error('Failed to load users:', error)
    }
  }

  const handleRoleChange = async (user: User, newRole: UserRole) => {
    setRoleChangeConfirm({
      isOpen: true,
      user,
      newRole
    })
  }

  const confirmRoleChange = async () => {
    if (!roleChangeConfirm.user || !roleChangeConfirm.newRole) return

    try {
      await updateUserRole({
        userId: roleChangeConfirm.user.id,
        newRole: roleChangeConfirm.newRole
      })
      
      setUsers(users.map(u => 
        u.id === roleChangeConfirm.user?.id 
          ? { ...u, role: roleChangeConfirm.newRole! }
          : u
      ))
      
      setRoleChangeConfirm({ isOpen: false, user: null, newRole: null })
    } catch (error) {
      console.error('Failed to update user role:', error)
    }
  }

  return (
    <div className="bg-white rounded-lg border border-gray-200">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Username</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Role</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Registration Date</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {users.map((user) => (
              <tr key={user.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {user.first_name} {user.last_name}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {user.email}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="relative">
                    <select
                      key={user.id}
                      value={user.role}
                      onChange={(e) => handleRoleChange(user, e.target.value as UserRole)}
                      className="appearance-none bg-white border border-gray-300 rounded-md pl-3 pr-8 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-[#1B3B36] focus:border-[#1B3B36]"
                    >
                      {USER_ROLES.map((role) => (
                        <option key={role} value={role}>
                          {role}
                        </option>
                      ))}
                    </select>
                    <ChevronDownIcon className="absolute right-2 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" />
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
                    ${user.auth ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {user.auth ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {format(new Date(user.created_at), 'dd/MM/yy')}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="flex justify-end p-4 border-t border-gray-200">
        <button
          className="inline-flex items-center px-3 py-2 text-sm font-medium text-[#1B3B36] hover:text-[#2C5C54]"
        >
          View All
          <svg className="ml-2 w-4 h-4" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
          </svg>
        </button>
      </div>

      <AnimatePresence>
        {roleChangeConfirm.isOpen && (
          <Dialog
            static
            as={motion.div}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            open={roleChangeConfirm.isOpen}
            onClose={() => setRoleChangeConfirm({ isOpen: false, user: null, newRole: null })}
            className="fixed inset-0 z-10 overflow-y-auto"
          >
            <div className="flex min-h-screen items-center justify-center p-4">
              <div className="fixed inset-0 bg-black/30" aria-hidden="true" />

              <motion.div
                initial={{ scale: 0.95 }}
                animate={{ scale: 1 }}
                exit={{ scale: 0.95 }}
                className="relative bg-white rounded-lg p-6 max-w-sm w-full"
              >
                <DialogTitle className="text-lg font-medium text-gray-900 mb-4">
                  Role Update
                </DialogTitle>
                <p className="text-sm text-gray-500 mb-4">
                  Change {roleChangeConfirm.user?.first_name}'s role
                </p>
                <p className="text-sm font-medium mb-6">
                  From: {roleChangeConfirm.user?.role.replace(/_/g, ' ')}{' '}
                  To: {roleChangeConfirm.newRole?.replace(/_/g, ' ')}
                </p>

                <div className="flex flex-col gap-2">
                  <button
                    type="button"
                    onClick={confirmRoleChange}
                    className="w-full px-4 py-2 text-sm font-medium text-white bg-[#1B3B36] rounded-md hover:bg-[#2C5C54] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#1B3B36]"
                  >
                    Confirm
                  </button>
                  <button
                    type="button"
                    onClick={() => setRoleChangeConfirm({ isOpen: false, user: null, newRole: null })}
                    className="w-full px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-[#1B3B36]"
                  >
                    Close
                  </button>
                </div>
              </motion.div>
            </div>
          </Dialog>
        )}
      </AnimatePresence>
    </div>
  )
} 