'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Tab } from '@headlessui/react'
import { UserManagement } from './tabs/UserManagement'
import { DeletionRequests } from './tabs/DeletionRequests'
import { MedicalTerms } from './tabs/MedicalTerms'
import { GlossaryRequests } from './tabs/GlossaryRequests'

const tabs = [
  { 
    name: 'Team Members', 
    component: UserManagement,
    count: 38,
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 4.354a4 4 0 110 5.292V4.354zM15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197L15 21zM13 7a4 4 0 11-8 0 4 4 0 018 0v0z" 
          stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
    )
  },
  { 
    name: 'Deletion Requests', 
    component: DeletionRequests,
    count: 11,
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" 
          stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
    )
  },
  { 
    name: 'Medical Terms', 
    component: MedicalTerms,
    count: 21,
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" 
          stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
    )
  },
  { 
    name: 'Glossary', 
    component: GlossaryRequests,
    count: 16,
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" 
          stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
    )
  },
]

export function AdminPanel() {
  const [selectedIndex, setSelectedIndex] = useState(0)

  return (
    <div className="w-full min-h-screen bg-white px-6 py-4">
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">Admin</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {tabs.map((tab, index) => {
          const isSelected = selectedIndex === index
          return (
            <button
              key={tab.name}
              onClick={() => setSelectedIndex(index)}
              className={`flex items-center justify-between p-4 rounded-lg transition-colors ${
                isSelected 
                  ? 'bg-[#1B3B36] text-white' 
                  : 'bg-white border border-gray-200 text-gray-900 hover:bg-gray-50'
              }`}
            >
              <div className="flex items-center gap-3">
                <span className={`${isSelected ? 'text-white' : 'text-[#1B3B36]'}`}>
                  {tab.icon}
                </span>
                <span className="text-sm font-medium">{tab.name}</span>
              </div>
              <span className="text-2xl font-semibold">{tab.count}</span>
            </button>
          )
        })}
      </div>

      <Tab.Group selectedIndex={selectedIndex} onChange={setSelectedIndex}>
        <Tab.Panels>
          <AnimatePresence mode="wait">
            {tabs.map((tab, idx) => (
              <Tab.Panel
                key={tab.name}
                static
                className={selectedIndex === idx ? 'block' : 'hidden'}
              >
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.2 }}
                >
                  <tab.component />
                </motion.div>
              </Tab.Panel>
            ))}
          </AnimatePresence>
        </Tab.Panels>
      </Tab.Group>
    </div>
  )
} 