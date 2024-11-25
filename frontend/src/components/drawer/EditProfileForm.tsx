"use client"

import React from 'react';
import {useSession} from 'next-auth/react';
import {useState, useTransition} from 'react';
import {updateUserProfile} from '@/actions/user';

interface EditProfileFormProps {
    onCancel: () => void;
}

const EditProfileForm = ({onCancel}: EditProfileFormProps) => {
    const {data: session, update} = useSession();
    const [isPending, startTransition] = useTransition();
    const [error, setError] = useState<string | null>(null);

    const [firstName, lastName] = session?.user?.name?.split(' ') || ['', ''];

    const [formData, setFormData] = useState({
        firstName,
        lastName,
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);

        startTransition(async () => {
            try {
                const result = await updateUserProfile({
                    first_name: `${formData.firstName}`.trim(),
                    last_name: `${formData.lastName}`.trim(),
                });

                if (result.success) {
                    await update({
                        ...session,
                        user: {
                            ...session?.user,
                            name: `${formData.firstName} ${formData.lastName}`.trim(),
                        },
                    });
                    onCancel();
                } else {
                    setError(result.error || 'Failed to update profile');
                }
            } catch (err) {
                setError('An unexpected error occurred');
                console.error('Error updating profile:', err);
            }
        });
    };

    return (
        <form onSubmit={handleSubmit} className="w-full max-w-md p-2">
            <h2 className="text-white text-xl font-urbanist mb-6 text-center">Edit Profile</h2>

            <div className="flex flex-col gap-5">
                {error && (
                    <div className="text-red-400 text-sm bg-red-900/20 p-3 rounded-lg">
                        {error}
                    </div>
                )}

                <div className="space-y-2">
                    <label className="text-white/90 text-sm font-urbanist block">
                        First Name
                    </label>
                    <input
                        type="text"
                        value={formData.firstName}
                        onChange={(e) => setFormData(prev => ({...prev, firstName: e.target.value}))}
                        className="w-full p-3 bg-[#244239] text-white border border-white/10 rounded-lg focus:border-white/30 focus:outline-none transition-colors"
                        placeholder="Enter your first name"
                        disabled={isPending}
                    />
                </div>

                <div className="space-y-2">
                    <label className="text-white/90 text-sm font-urbanist block">
                        Last Name
                    </label>
                    <input
                        type="text"
                        value={formData.lastName}
                        onChange={(e) => setFormData(prev => ({...prev, lastName: e.target.value}))}
                        className="w-full p-3 bg-[#244239] text-white border border-white/10 rounded-lg focus:border-white/30 focus:outline-none transition-colors"
                        placeholder="Enter your last name"
                        disabled={isPending}
                    />
                </div>

                <div className="flex justify-end gap-3 mt-4">
                    <button
                        type="button"
                        onClick={onCancel}
                        className="px-6 py-2.5 text-white/90 border border-white/10 rounded-full hover:bg-[#244239] transition-colors disabled:opacity-50 font-urbanist text-sm"
                        disabled={isPending}
                    >
                        Cancel
                    </button>
                    <button
                        type="submit"
                        className="px-6 py-2.5 text-white bg-[#2A4E44] border border-white/10 rounded-full hover:bg-[#2A4E44]/80 transition-colors disabled:opacity-50 font-urbanist text-sm"
                        disabled={isPending}
                    >
                        {isPending ? 'Saving...' : 'Save Changes'}
                    </button>
                </div>
            </div>
        </form>
    );
};

export default EditProfileForm; 