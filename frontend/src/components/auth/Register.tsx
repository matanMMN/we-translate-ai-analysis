'use client'

import Link from 'next/link'
import {Mail, Lock, User} from 'lucide-react'
import {Button} from '@/components/ui/button'
import {Input} from '@/components/ui/input'
import {Checkbox} from '@/components/ui/checkbox'
import {Label} from '@/components/ui/label'

export default function Register() {
    return (
        <div className="flex items-center justify-center p-8">
            <div className="w-full max-w-[400px] space-y-6">
                <div className="space-y-2">
                    <h1 className="text-2xl font-semibold tracking-tight">Create an account</h1>
                    <p className="text-sm text-muted-foreground">
                        Already have an account?{' '}
                        <Link href="/login" className="text-[#1F3B33] hover:underline">
                            Log in
                        </Link>
                    </p>
                </div>

                <div className="space-y-4">
                    <div className="space-y-2">
                        <Label htmlFor="name">Full Name</Label>
                        <div className="relative">
                            <User className="absolute left-3 top-2.5 h-5 w-5 text-muted-foreground"/>
                            <Input
                                id="name"
                                placeholder="Enter full name"
                                className="pl-10"
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="email">Email</Label>
                        <div className="relative">
                            <Mail className="absolute left-3 top-2.5 h-5 w-5 text-muted-foreground"/>
                            <Input
                                id="email"
                                type="email"
                                placeholder="Enter email"
                                className="pl-10"
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="password">Password</Label>
                        <div className="relative">
                            <Lock className="absolute left-3 top-2.5 h-5 w-5 text-muted-foreground"/>
                            <Input
                                id="password"
                                type="password"
                                placeholder="Enter password"
                                className="pl-10"
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="confirm-password">Confirm Password</Label>
                        <div className="relative">
                            <Lock className="absolute left-3 top-2.5 h-5 w-5 text-muted-foreground"/>
                            <Input
                                id="confirm-password"
                                type="password"
                                placeholder="Confirm password"
                                className="pl-10"
                            />
                        </div>
                    </div>

                    <div className="flex items-center space-x-2">
                        <Checkbox id="terms"/>
                        <label
                            htmlFor="terms"
                            className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                        >
                            I agree to the{' '}
                            <Link href="/terms" className="text-[#1F3B33] hover:underline">
                                terms and conditions
                            </Link>
                        </label>
                    </div>

                    <Button className="w-full bg-[#1F3B33] hover:bg-[#2a4f44]">
                        REGISTER
                    </Button>
                </div>
            </div>
        </div>
    )
}