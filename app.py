import React from 'react';

export const Header: React.FC = () => {
  return (
    <header className="bg-white border-b border-slate-100 p-4 sm:p-5 flex items-center justify-between z-10 sticky top-0">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-brand-500 flex items-center justify-center text-white font-bold shadow-md">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-6 h-6">
            <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z" />
          </svg>
        </div>
        <div>
          <h1 className="text-xl font-bold text-slate-800 tracking-tight">SoCalBid</h1>
          <p className="text-xs text-brand-600 font-medium bg-brand-50 px-2 py-0.5 rounded-full inline-block mt-0.5">Online Auction Assistant</p>
        </div>
      </div>
      <div className="hidden sm:block text-right">
        <p className="text-xs text-slate-500 font-medium">Support Hours</p>
        <p className="text-sm font-semibold text-slate-700">10am - 4pm</p>
      </div>
    </header>
  );
};
