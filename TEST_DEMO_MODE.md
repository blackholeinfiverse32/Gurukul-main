# Demo Mode Testing Guide

## How to Test Demo Mode

### Step 1: Start the Services
```bash
START_DEMO.bat
```

### Step 2: Open Browser
Navigate to: http://localhost:5173

### Step 3: Test Demo Mode
1. Click "Sign In" button
2. Click "Continue in Demo Mode" button
3. Should redirect to /home dashboard
4. Should see dashboard content

### Expected Behavior
- ✅ Button click sets localStorage.setItem('demoMode', 'true')
- ✅ Redux store updated with demo user
- ✅ Toast notification shows "Accessing in demo mode"
- ✅ Redirects to /home
- ✅ ProtectedRoute allows access
- ✅ Dashboard loads successfully

### Troubleshooting

#### Issue: Redirects back to sign-in
**Check**: Open browser console (F12)
**Look for**: localStorage.getItem('demoMode')
**Should be**: 'true'

**Fix**: Clear localStorage and try again
```javascript
localStorage.clear()
```

#### Issue: Dashboard doesn't load
**Check**: Browser console for errors
**Common causes**:
- Backend not running
- API endpoints not configured
- CORS errors

**Fix**: 
1. Ensure backend is running on port 8000
2. Check .env has correct API URLs
3. Restart both services

#### Issue: Button doesn't work
**Check**: Browser console for JavaScript errors
**Look for**: Redux dispatch errors

**Fix**: Ensure all dependencies installed
```bash
cd "Gurukul_new-main\new frontend"
npm install
```

### Manual Demo Mode Activation

If button doesn't work, manually activate:

1. Open browser console (F12)
2. Run:
```javascript
localStorage.setItem('demoMode', 'true');
window.location.href = '/home';
```

### Verify Demo Mode is Active

In browser console:
```javascript
localStorage.getItem('demoMode')
// Should return: "true"
```

### Disable Demo Mode

In browser console:
```javascript
localStorage.removeItem('demoMode');
// Or clear all:
localStorage.clear();
```

Then refresh the page.

## Testing Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] Can access sign-in page
- [ ] "Continue in Demo Mode" button visible
- [ ] Button click shows toast notification
- [ ] Redirects to /home
- [ ] Dashboard loads without errors
- [ ] Can navigate to other pages
- [ ] localStorage has demoMode=true
- [ ] Redux store has demo user

## Success Criteria

Demo mode is working if:
1. ✅ Click button on sign-in page
2. ✅ See success toast
3. ✅ Redirect to dashboard
4. ✅ Dashboard content visible
5. ✅ Can use all features
6. ✅ No authentication errors

## Common Errors and Solutions

### Error: "RedirectToSignIn"
**Cause**: ProtectedRoute not detecting demo mode
**Solution**: Check localStorage has 'demoMode' = 'true'

### Error: "Cannot read property 'dispatch'"
**Cause**: Redux not properly initialized
**Solution**: Check store.js is imported in main.jsx

### Error: "Network Error"
**Cause**: Backend not running or CORS issue
**Solution**: 
1. Start backend: `cd Backend && python main.py`
2. Check CORS in backend .env

### Error: Page blank after redirect
**Cause**: Dashboard component error
**Solution**: Check browser console for component errors

## Quick Test Script

Run in browser console after clicking demo mode:

```javascript
// Check demo mode
console.log('Demo Mode:', localStorage.getItem('demoMode'));

// Check current path
console.log('Current Path:', window.location.pathname);

// Check Redux state (if Redux DevTools installed)
// Look for auth.user with id: 'demo-user'
```

## Expected Console Output

After clicking "Continue in Demo Mode":
```
✅ Toast: "Accessing in demo mode"
✅ localStorage.demoMode: "true"
✅ Redux auth.user: { id: 'demo-user', email: 'demo@gurukul.com', ... }
✅ Navigation: /home
✅ No errors in console
```

## If All Else Fails

1. Clear browser cache and localStorage
2. Restart both backend and frontend
3. Try in incognito/private window
4. Check all files were saved correctly
5. Verify npm install completed successfully
