//ログインAPI
///
// @router.post("/login", response_model=UserResponse)
// def login(user_id: str, db: Session = Depends(get_db)):
//     users = (
//         db.query(USERS.user_id, USERS.is_admin).filter(USERS.user_id == user_id).all()
//     )
//     return users

import axios from 'axios';
const API_BASE_URL = 'http://localhost:8000/api/users'; // FastAPIのベースURL

// ログイン関数
export const login = async (user_id: any) => {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/login`,  user_id
      );
      return response.data;
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };