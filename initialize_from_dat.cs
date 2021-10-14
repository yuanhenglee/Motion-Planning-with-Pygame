using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;


public class initialize_from_dat : MonoBehaviour
{
    public Material robot_material;
    public Material obstacle_material;
    int n_robots;
    int n_obstacles;

    Robot[] robots;
    Obstacle[] obstacles;
    // Start is called before the first frame update
    void Start()
    {
        loadRobot();

        placeRobots();

        // loadObstacle();

        // placeObstacles();
    }

    // Read dat form robot.dat file
    void loadRobot()
    {
        string path = "Assets/robot.dat";
        //Read the text from directly from the test.txt file

        using (StreamReader sr = new StreamReader(path))
        {
            string title_line = sr.ReadLine();
            n_robots = int.Parse(sr.ReadLine());
            robots = new Robot[n_robots];
            for (int i = 0; i < n_robots; ++i)
            {
                title_line = sr.ReadLine();
                title_line = sr.ReadLine();
                int n_convex = int.Parse(sr.ReadLine());
                Convex[] parts = new Convex[n_convex];
                for (int j = 0; j < n_convex; ++j)
                {
                    title_line = sr.ReadLine();
                    title_line = sr.ReadLine();
                    int n_vertices = int.Parse(sr.ReadLine());
                    title_line = sr.ReadLine();
                    Vector3[] vertices = new Vector3[n_vertices];
                    for (int k = 0; k < n_vertices; ++k)
                    {
                        string[] subs = sr.ReadLine().Split(' ');
                        vertices[k] = new Vector3(float.Parse(subs[0]), 3.0f, float.Parse(subs[1]));
                    }
                    parts[j] = new Convex(n_vertices, vertices);

                }

                // Construct robot #i
                robots[i] = new Robot(i, n_convex, parts);

            }
            foreach (Robot r in robots)
            {
                print(r);
            }


        }
    }

    void placeRobots()
    {
        Mesh mesh = new Mesh();
        // TEMP just for testing
        mesh.vertices = robots[0].parts[0].vertices;

        int[] indices = new int[mesh.vertices.Length];
        for (int i = 0; i < mesh.vertices.Length; ++i)
        {
            indices[i] = i;
        }
        mesh.SetIndices(indices, MeshTopology.Points, 0);
        mesh.RecalculateBounds();
        Debug.Log(mesh.bounds);
        // int[] triangles = new int[12];
        // triangles[0] = 5;
        // triangles[1] = 1;
        // triangles[2] = 0;
        // triangles[3] = 5;
        // triangles[4] = 2;
        // triangles[5] = 1;
        // triangles[6] = 5;
        // triangles[7] = 4;
        // triangles[8] = 2;
        // triangles[9] = 4;
        // triangles[10] = 2;
        // triangles[11] = 3;

        // mesh.triangles = triangles;

        GameObject r = new GameObject("Robot0", typeof(MeshFilter), typeof(MeshRenderer));
        r.GetComponent<MeshFilter>().mesh = mesh;
        // r.GetComponent<MeshRenderer>().material = robot_material;


    }

    // Read dat form robot.dat file
    void loadObstacle()
    {
        string path = "Assets/obstacle.dat";
        //Read the text from directly from the test.txt file

        using (StreamReader sr = new StreamReader(path))
        {
            string title_line = sr.ReadLine();
            n_obstacles = int.Parse(sr.ReadLine());
            obstacles = new Obstacle[n_obstacles];
            for (int i = 0; i < n_obstacles; ++i)
            {
                title_line = sr.ReadLine();
                title_line = sr.ReadLine();
                int n_convex = int.Parse(sr.ReadLine());
                Convex[] parts = new Convex[n_convex];
                for (int j = 0; j < n_convex; ++j)
                {
                    title_line = sr.ReadLine();
                    title_line = sr.ReadLine();
                    int n_vertices = int.Parse(sr.ReadLine());
                    title_line = sr.ReadLine();
                    Vector3[] vertices = new Vector3[n_vertices];
                    for (int k = 0; k < n_vertices; ++k)
                    {
                        string[] subs = sr.ReadLine().Split(' ');
                        vertices[k] = new Vector3(float.Parse(subs[0]), 3.0f, float.Parse(subs[1]));
                    }
                    parts[j] = new Convex(n_vertices, vertices);

                }

                // Construct obstacle #i
                obstacles[i] = new Obstacle(i, n_convex, parts);

                print("complete obstacle #" + i);
            }
            foreach (Obstacle r in obstacles)
            {
                print(r);
            }


        }
    }
    void placeObstacles()
    {
        Mesh mesh = new Mesh();
        // TEMP just for testing
        mesh.vertices = obstacles[0].parts[0].vertices;


        // mesh.triangles = triangles;

        GameObject r = new GameObject("Obstacle0", typeof(MeshFilter), typeof(MeshRenderer));
        r.GetComponent<MeshFilter>().mesh = mesh;
        r.GetComponent<MeshRenderer>().material = obstacle_material;


    }
}
