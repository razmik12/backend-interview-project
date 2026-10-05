import pytest
from httpx import AsyncClient





@pytest.mark.asyncio
async def test_create_projects(client:AsyncClient,login_user_two,projects_data:dict[str:str]):
    token = login_user_two["access_token"]
    
    response = await client.post("/projects",
                                 json=projects_data,
                                 headers={ "Authorization": f"Bearer {token}"})
    assert response.status_code == 201  
    response = response.json()
    assert "name" in response
    assert "description" in response
    assert "owner_id" in response
    
    
    
@pytest.mark.asyncio
async def test_create_project_unauthorized(client:AsyncClient):

    
    response = await client.post("/projects",
                                 json={"name":"project_new",
                                       "description":"new_description"},
                                 )
    assert response.status_code == 401  
    
    
    
@pytest.mark.parametrize(
    ("name,description"),
    [
    ("","check_description"),
    ("",""),
        
    ],
)

@pytest.mark.asyncio
async def test_create_project_invalid_data(client:AsyncClient,
                                       login_user_two,
                                       name,
                                       description,                
                                       ):

    token = login_user_two["access_token"]
    response = await client.post("/projects",
                                 json={"name":name,
                                       "description":description},
                                 headers={"Authorization": f"Bearer {token}"}
                                 )
    assert response.status_code == 422  
    

@pytest.mark.asyncio
async def test_list_projects(client:AsyncClient,
                             login_user_two,
                             created_project):
    token = login_user_two["access_token"]
    response = await client.get(url="/projects",
                                headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    projects = response.json()
    
    assert len(projects) == 1
    assert projects[0]["id"] == created_project["id"]
    assert projects[0]["name"] == created_project["name"]
    

@pytest.mark.asyncio
async def test_get_projects_id(client:AsyncClient,
                               login_user_two,
                               created_project):
    project_id = created_project["id"]
    token = login_user_two["access_token"]
    response = await client.get(url=f"/projects/{project_id}",
                                headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    project = response.json()
    
    assert project["id"] == created_project["id"]
    assert project["owner_id"] == created_project["owner_id"]
    assert project["name"] == created_project["name"]
    

@pytest.mark.asyncio
async def test_add_member(client:AsyncClient,
                          login_user_two,
                          created_project,
                          user):
      project_id = created_project["id"]
      token = login_user_two["access_token"]
      user_id = user["id"]
      response = await client.post(url=f"/projects/{project_id}/members",
                                   headers={"Authorization": f"Bearer {token}"},
                                   json={"user_id":user_id}
                                   )
      assert response.status_code == 201
      member = response.json()
      
      assert member["project_id"] == created_project["id"]
      assert member["role"] == "member"
      assert member["user_id"] == user_id
      
      
      
      
      
@pytest.mark.asyncio
async def test_get_projects_with_new_member(client:AsyncClient,
                          login_user_two,
                          created_project,
                          user):
   
      project_id = created_project["id"]
      token = login_user_two["access_token"]
      user_id = user["id"]
      response = await client.post(url=f"/projects/{project_id}/members",
                                   headers={"Authorization": f"Bearer {token}"},
                                   json={"user_id":user_id}
                                   )
      assert response.status_code == 201
      member = response.json()
      
      assert member["project_id"] == created_project["id"]
      assert member["role"] == "member"
      assert member["user_id"] == user_id    
      
      duplicate_response = await client.get(url=f"/projects/{project_id}",
                                            headers={"Authorization": f"Bearer {token}"}) 
      assert duplicate_response.status_code == 200
      project = duplicate_response.json()
      members = project["members"]
      assert len(members) == 2
      
      
      
      
      
      
      
      
      
@pytest.mark.asyncio
async def test_add_member_error(client:AsyncClient,
                          login_user_two,
                          created_project,
                          ):
      project_id = created_project["id"]
      token = login_user_two["access_token"]
      response = await client.post(url=f"/projects/{project_id}/members",
                                   headers={"Authorization": f"Bearer {token}"},
                                   json={"user_id":"00000000-0000-0000-0000-000000000000"}
                                   )
      assert response.status_code == 404
      
      
      
      
@pytest.mark.asyncio
async def test_add_member_error_owner(client:AsyncClient,
                          login_user,
                          created_project,
                          user):
      project_id = created_project["id"]
      token = login_user["access_token"]
      user_id = user["id"]
      response = await client.post(url=f"/projects/{project_id}/members",
                                   headers={"Authorization": f"Bearer {token}"},
                                   json={"user_id":user_id}
                                   )
      assert response.status_code == 403
      

@pytest.mark.asyncio
async def test_get_projects_id_forbidden_for_non_member(client: AsyncClient, login_user, created_project):
    project_id = created_project["id"]
    token = login_user["access_token"]   
    response = await client.get(url=f"/projects/{project_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_add_member_error_duplicate_member(client:AsyncClient,
                                                 login_user_two,
                                                created_project,
                                                user):
          project_id = created_project["id"]
          token = login_user_two["access_token"]
          user_id = user["id"]
          response = await client.post(url=f"/projects/{project_id}/members",
                                       headers={"Authorization": f"Bearer {token}"},
                                       json={"user_id":user_id}
                                       )
          assert response.status_code == 201
          
          duplicate_response = await client.post(url=f"/projects/{project_id}/members",
                                       headers={"Authorization": f"Bearer {token}"},
                                       json={"user_id":user_id}
                                       )
          
          assert duplicate_response.status_code == 409



@pytest.mark.asyncio
async def test_update_project_owner(client: AsyncClient,
                                     login_user_two,
                                     created_project):
    project_id = created_project["id"]
    token = login_user_two["access_token"]

    response = await client.patch(url=f"/projects/{project_id}",
                                   headers={"Authorization": f"Bearer {token}"},
                                   json={"name": "Updated Name"})
    assert response.status_code == 200
    project = response.json()

    assert project["name"] == "Updated Name"
    assert project["description"] == created_project["description"] 


@pytest.mark.asyncio
async def test_update_project_forbidden(client: AsyncClient,
                                         login_user,
                                         created_project):
    project_id = created_project["id"]
    token = login_user["access_token"]   

    response = await client.patch(url=f"/projects/{project_id}",
                                   headers={"Authorization": f"Bearer {token}"},
                                   json={"name": "Hacked Name"})
    assert response.status_code == 403
    
    
    
@pytest.mark.asyncio
async def test_delete_project_owner(client: AsyncClient,
                                     login_user_two,
                                     created_project):
    project_id = created_project["id"]
    token = login_user_two["access_token"]

    response = await client.delete(url=f"/projects/{project_id}",
                                  headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204

    response = await client.get(url=f"/projects/{project_id}",
                                 headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_project_forbidden(client: AsyncClient,
                                         login_user,
                                         created_project):
    project_id = created_project["id"]
    token = login_user["access_token"]   
    response = await client.delete(url=f"/projects/{project_id}",
                                    headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
    
    
    
